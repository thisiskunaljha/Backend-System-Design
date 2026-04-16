# Community Feed

A modern Django community platform with user authentication, feed functionality, comments, and social features.

## Features

✨ **Core Features:**
- 📝 Create and share posts
- 💬 Nested comments with replies
- 👍 Like/unlike posts and comments
- 👤 User profiles with stats
- 🏆 Leaderboard system with karma tracking
- 🔐 Secure user authentication
- 🔑 **Google OAuth login** (ready to use!)
- 📱 REST API for all features
- 🎨 Beautiful dark-themed UI

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/thisiskunaljha/Backend-System-Design.git
cd Backend-System-Design

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
cd community
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit: http://localhost:8000

### Setup Google OAuth (Optional)

To enable Google login, you have two options:

**Option 1: Automated Setup (Recommended)**

```bash
python manage.py setup_google_oauth
```

This will prompt you for your Google OAuth credentials and configure everything automatically.

**Option 2: Manual Setup**

See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) for detailed instructions.

## Google Login (via django-allauth)

### Prerequisites

- Ensure these are installed:
  - `django-allauth` (included in requirements.txt)
  - `requests`
  - `cryptography`

### Configuration

1. **Get Google OAuth Credentials**
   - Go to https://console.cloud.google.com/apis/credentials
   - Create OAuth 2.0 Client ID (Web application)
   - Add authorized redirect URI:
     - `http://localhost:8000/accounts/google/login/callback/`
     - `https://<your-domain>/accounts/google/login/callback/` (production)

2. **Setup Using Management Command** (Recommended)
   ```bash
   python manage.py setup_google_oauth --client-id YOUR_CLIENT_ID --secret YOUR_SECRET
   ```
   
   Or run interactively:
   ```bash
   python manage.py setup_google_oauth
   ```

3. **Alternative: Manual Setup via Admin**
   - Go to http://localhost:8000/admin/
   - Under "Social Accounts" → "Social Applications"
   - Add a new Social App:
     - Provider: Google
     - Name: Google
     - Client ID: `<your-client-id>`
     - Secret: `<your-client-secret>`
     - Sites: Select your site

4. **Start Using Google Login**
   - Go to http://localhost:8000/login/
   - Click "✓ Continue with Google"

### Environment Variables (Production)

For production deployment, set these environment variables:

```bash
SOCIAL_AUTH_GOOGLE_CLIENT_ID=your_client_id
SOCIAL_AUTH_GOOGLE_SECRET=your_client_secret
```

## API Endpoints

All endpoints support both session and token authentication.

### Posts
- `POST /posts/` - Create a new post
- `GET /posts/<id>/` - Get post details with comments

### Comments
- `POST /comments/` - Create a comment on a post
- `POST /comments/` - Reply to existing comments

### Likes
- `POST /likes/` - Toggle like/unlike on posts or comments

### Leaderboard
- `GET /leaderboard/` - Get top 5 users by karma

### JSON Feed
- `GET /posts-json/` - Get all posts as JSON

## Web Pages

- `/` - Main feed (home page)
- `/login/` - Login with username/password or Google
- `/signup/` - Register new account
- `/profile/` - Your profile
- `/profile/<username>/` - View other user's profile
- `/admin/` - Django admin panel

## Karma System

Users earn karma points:
- 5 points per post like
- 1 point per comment like

Karma is tracked in the last 24 hours on the leaderboard.

## Development

### Run Tests
```bash
python manage.py test feed
```

### Create Sample Data
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from feed.models import Post, Comment, Like
>>> user = User.objects.create_user(username='testuser', password='pass123')
>>> post = Post.objects.create(author=user, content='Hello World!')
```

### Database Migrations
```bash
# Create migrations for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## Deployment

### Render.com

1. Connect your GitHub repository
2. Set environment variables:
   - `SECRET_KEY` - Generate one
   - `DEBUG` - Set to 0
   - `DATABASE_URL` - Your PostgreSQL URL
   - `SOCIAL_AUTH_GOOGLE_CLIENT_ID` - Your Google Client ID
   - `SOCIAL_AUTH_GOOGLE_SECRET` - Your Google Secret
3. Run build command: `bash ./build.sh`
4. Start command: `gunicorn --chdir community community.wsgi`

### Heroku

```bash
# Add environment variables
heroku config:set SOCIAL_AUTH_GOOGLE_CLIENT_ID=your_id
heroku config:set SOCIAL_AUTH_GOOGLE_SECRET=your_secret

# Deploy
git push heroku main
```

## Troubleshooting

### Google Login Shows "Redirect URI mismatch"
- Check your site domain in `/admin/sites/`
- Update authorized redirect URIs in Google Cloud Console
- Run `python manage.py setup_google_oauth` again

### Can't Login With Google
- Make sure Social Application is created in Django Admin
- Verify Site is associated with the Social App
- Check that Client ID and Secret are correct

### Database Issues
```bash
# Reset database (development only)
rm community/db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django Auth + django-allauth (Google OAuth)
- **Server**: Gunicorn + WhiteNoise
- **Static Files**: CollectStatic with WhiteNoise compression

## Project Structure

```
community/
├── manage.py
├── db.sqlite3
├── community/           # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── feed/               # Main app
│   ├── models.py       # Post, Comment, Like models
│   ├── views.py        # API and view endpoints
│   ├── serializers.py  # DRF serializers
│   ├── urls.py         # App URLs
│   ├── admin.py        # Admin configuration
│   ├── migrations/     # Database migrations
│   ├── management/
│   │   └── commands/
│   │       └── setup_google_oauth.py  # OAuth setup command
│   └── templates/      # HTML templates
└── staticfiles/        # Collected static files
```

## Documentation

- [Complete Google OAuth Setup Guide](GOOGLE_OAUTH_SETUP.md)
- [Project Status](PROJECT_STATUS.md)
- [Django Documentation](https://docs.djangoproject.com/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)
3. Check Django and django-allauth documentation
4. Create an issue on GitHub

### 6. Use in UI

- Go to `/login/` for local login
- Go to `/accounts/login/` for allauth login with Google
- Google button will send users to Google OAuth sign-in

