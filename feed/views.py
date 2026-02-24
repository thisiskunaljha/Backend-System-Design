from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from datetime import timedelta
from django.db import IntegrityError
from django.db.models import Sum, Case, When, IntegerField, Count
from django.http import JsonResponse

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentCreateSerializer





class PostCreateView(APIView):
    def post(self, request):
        content = request.data.get("content", "").strip()
        if not content:
            return Response(
                {"error": "Content cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is authenticated (session or token)
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        post = Post.objects.create(
            content=content,
            author=request.user
        )
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(
            Post.objects
            .select_related("author")
            .prefetch_related("comments__replies")
            .get(id=post_id)
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentCreateView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user)
            return Response({"id": comment.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        post_id = request.data.get("post")
        comment_id = request.data.get("comment")

        # Check if user already liked this post/comment
        existing_like = Like.objects.filter(
            user=request.user,
            post_id=post_id,
            comment_id=comment_id
        ).first()
        
        if existing_like:
            # Unlike (delete the like)
            existing_like.delete()
            status_code = status.HTTP_200_OK
            action = "unliked"
        else:
            # Like (create a new like)
            try:
                Like.objects.create(
                    user=request.user,
                    post_id=post_id,
                    comment_id=comment_id
                )
                status_code = status.HTTP_201_CREATED
                action = "liked"
            except IntegrityError:
                return Response(
                    {"detail": "Error creating like"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Return updated like count
        if post_id:
            like_count = Like.objects.filter(post_id=post_id).count()
        else:
            like_count = Like.objects.filter(comment_id=comment_id).count()

        return Response(
            {"status": action, "like_count": like_count},
            status=status_code
        )


def karma_last_24h():
    since = now() - timedelta(hours=24)

    post_likes = (
        Like.objects
        .filter(post__isnull=False, created_at__gte=since)
        .values("post__author")
        .annotate(score=Count("id") * 5)
    )

    comment_likes = (
        Like.objects
        .filter(comment__isnull=False, created_at__gte=since)
        .values("comment__author")
        .annotate(score=Count("id"))
    )

    return post_likes, comment_likes

class LeaderboardView(APIView):
    def get(self, request):
        last_24h = now() - timedelta(hours=24)

        leaderboard = (
            Like.objects
            .filter(created_at__gte=last_24h)
            .values("user__username")
            .annotate(
                karma=Sum(
                    Case(
                        When(post__isnull=False, then=5),
                        When(comment__isnull=False, then=1),
                        output_field=IntegerField()
                    )
                )
            )
            .order_by("-karma")[:5]
        )

        return Response(leaderboard)


def feed(request):
    posts = Post.objects.select_related("author").prefetch_related(
        "comments", "comments__author"
    ).all().order_by("-created_at")
    return render(request, 'feed/feed.html', {"posts": posts})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'feed/signup.html', {'form': form})


def posts_json(request):
    posts = Post.objects.select_related("author").prefetch_related(
        "comments", "comments__author", "likes"
    ).all().order_by("-created_at")
    
    data = []
    for post in posts:
        comments_data = []
        for comment in post.comments.filter(parent__isnull=True):
            comments_data.append({
                "id": comment.id,
                "author": comment.author.username if comment.author else "Anonymous",
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                "replies": [
                    {
                        "id": reply.id,
                        "author": reply.author.username if reply.author else "Anonymous",
                        "content": reply.content,
                        "created_at": reply.created_at.strftime("%Y-%m-%d %H:%M"),
                    }
                    for reply in comment.replies.all()
                ]
            })
        
        data.append({
            "id": post.id,
            "author": post.author.username if post.author else "Anonymous",
            "content": post.content,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
            "like_count": post.likes.count(),
            "comments": comments_data
        })
    
    return JsonResponse(data, safe=False)

