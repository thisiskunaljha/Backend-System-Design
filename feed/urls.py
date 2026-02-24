from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import (
    PostCreateView,
    PostDetailView,
    CommentCreateView,
    LikeView,
    LeaderboardView
)

urlpatterns = [
    # Auth views
    path('', views.feed, name='home'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # API endpoints
    path('posts/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('likes/', LikeView.as_view(), name='like'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    
    # JSON endpoints
    path('posts-json/', views.posts_json, name='posts_json'),
]
