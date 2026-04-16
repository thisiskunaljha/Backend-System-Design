# Environment Variables Setup Guide

## 🔐 Security Best Practices

This application uses environment variables to securely manage sensitive credentials. **Never commit `.env` files to version control.**

## 📋 Required Environment Variables

### 1. Copy the Example File
```bash
cp .env.example .env
```

### 2. Generate Django Secret Key
For development, you can use the provided insecure key in `.env`. For production:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and set `SECRET_KEY` in `.env`.

### 3. Google OAuth Setup

#### Step 1: Create Google OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new OAuth 2.0 Client ID:
   - Application type: **Web application**
   - Name: "Community Feed"
   - Authorized JavaScript origins: 
     - `http://localhost:8000`
     - `http://127.0.0.1:8000`
     - Your production domain (if applicable)
   - Authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/`
     - `http://127.0.0.1:8000/accounts/google/login/callback/`
     - `https://yourdomain.com/accounts/google/login/callback/` (production)

#### Step 2: Add Credentials to .env
```env
SOCIAL_AUTH_GOOGLE_CLIENT_ID=your_client_id_here
SOCIAL_AUTH_GOOGLE_SECRET=your_client_secret_here
```

#### Step 3: Configure in Django
Load the environment variables:
```bash
export $(cat .env | xargs)
cd community
python manage.py setup_google_oauth
```

Or run interactively:
```bash
cd community
python manage.py setup_google_oauth --client-id YOUR_ID --secret YOUR_SECRET
```

## 🚀 Development Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your Google OAuth credentials

# 5. Load environment variables
export $(cat .env | xargs)

# 6. Apply migrations
cd community
python manage.py migrate

# 7. Configure Google OAuth
python manage.py setup_google_oauth

# 8. Create superuser (optional)
python manage.py createsuperuser

# 9. Run development server
python manage.py runserver
```

## 🔍 Verify Configuration

```bash
cd community

# Check system configuration
python manage.py check

# List registered sites
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> print(Site.objects.all())
>>> from allauth.socialaccount.models import SocialApp
>>> print(SocialApp.objects.filter(provider='google'))
```

## 🛡️ Production Security

When deploying to production:

1. **Generate a new SECRET_KEY:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Set DEBUG=False** (disables detailed error pages)

3. **Enable HTTPS** - Set in environment:
   ```env
   DEBUG=0
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   CSRF_TRUSTED_ORIGIN=https://yourdomain.com
   ```

4. **Use a production database** - PostgreSQL recommended:
   ```env
   DATABASE_URL=postgresql://user:password@host:5432/database_name
   ```

5. **Store secrets in:**
   - Environment variables (recommended)
   - Managed secrets service (AWS Secrets Manager, Azure Key Vault, etc.)
   - Never hardcode credentials

6. **Update Google OAuth redirect URIs** to use your production domain

## 📝 Environment Variable Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key (generate a new one for production) |
| `DEBUG` | No | Set to `0` for production, `1` for development |
| `ALLOWED_HOSTS` | No | Comma-separated list of allowed hostnames |
| `DATABASE_URL` | No | Database connection string (defaults to SQLite) |
| `SOCIAL_AUTH_GOOGLE_CLIENT_ID` | For OAuth | Google OAuth Client ID |
| `SOCIAL_AUTH_GOOGLE_SECRET` | For OAuth | Google OAuth Client Secret |
| `CSRF_TRUSTED_ORIGIN` | For production | CSRF trusted origin for POST requests |

## ✅ Security Checklist

- [x] `.env` file is gitignored
- [x] Credentials stored in environment variables
- [x] No credentials in source code
- [x] SECRET_KEY regenerated for production
- [x] DEBUG=False in production
- [x] HTTPS enabled in production
- [x] Database credentials secured
- [x] Google OAuth URIs updated for production domain

## 🆘 Troubleshooting

### "CSRF validation failed"
- Ensure `CSRF_TRUSTED_ORIGINS` includes your domain with scheme (http:// or https://)

### "Google login returns error"
- Check that Google OAuth Client ID and Secret are correct in `.env`
- Verify authorized redirect URIs in Google Cloud Console
- Run `python manage.py setup_google_oauth` after updating credentials

### "Site matching query does not exist"
```bash
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> Site.objects.all().delete()
>>> exit()
# Then run: python manage.py setup_google_oauth
```

## 📚 References

- [Django Environment Variables](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth Setup](https://console.cloud.google.com/apis/credentials)
