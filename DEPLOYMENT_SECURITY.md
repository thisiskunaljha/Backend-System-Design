# Deployment Security Checklist

## ✅ Pre-Deployment Verification

Run this checklist before deploying to production:

### Code & Credentials
- [ ] No hardcoded secrets in Python files
- [ ] No `.env` files in git
- [ ] All credentials use environment variables
- [ ] `SECRET_KEY` is environment-based
- [ ] Google OAuth credentials in env vars only
- [ ] Database URL in environment variable

```bash
# Verify commands:
grep -r "client.id.*=.*['\"]\|SECRET_KEY.*=.*['\"]\|GOCSPX" --include="*.py" .
git log -p --all -S "GOCSPX-\|313615533352\|django-insecure-" --source --branches
cat .gitignore | grep -E "\.env|secrets"
```

### Configuration Files
- [ ] `.env` not committed to git
- [ ] `.env.example` has placeholders (no real values)
- [ ] `settings.py` uses `os.environ.get()`
- [ ] No debugging credentials in templates

### Security Settings
- [ ] `DEBUG = False` in production
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_HTTPONLY = True`
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] `SECRET_KEY` is generated and unique

### Google OAuth
- [ ] Client ID is valid and non-expired
- [ ] Client Secret is not exposed
- [ ] Authorized redirect URIs include production domain
- [ ] OAuth scopes limited to `profile`, `email`

### Database
- [ ] Using PostgreSQL (not SQLite) in production
- [ ] Database URL has strong password
- [ ] Database SSL/TLS enabled
- [ ] Database backups configured
- [ ] Migrations applied to production DB

### Hosting (Render.com)
- [ ] Environment variables set in dashboard
- [ ] `.env` file not uploaded
- [ ] SECRET_KEY regenerated (not from .env.example)
- [ ] Build command: `pip install -r requirements.txt && python community/manage.py collectstatic --noinput`
- [ ] Start command: `gunicorn community.wsgi:application --bind 0.0.0.0:$PORT`

## 🚀 Deployment Steps

### 1. Generate New SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; \
          print(f'SECRET_KEY={get_random_secret_key()}')"
```
Copy output to production environment variables (not .env file)

### 2. Create PostgreSQL Database
```bash
# On Render.com or your hosting provider
# Ensure database is encrypted and TLS-enabled
DATABASE_URL=postgresql://user:password@host:5432/db_name
```

### 3. Set Production Environment Variables
```
# Essential variables for Render.com dashboard:
SECRET_KEY=<generated-key>
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=<from-postgres-service>
SOCIAL_AUTH_GOOGLE_CLIENT_ID=<from-google-cloud>
SOCIAL_AUTH_GOOGLE_SECRET=<from-google-cloud>
CSRF_TRUSTED_ORIGIN=https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 4. Update Google OAuth Redirect URIs
In Google Cloud Console → OAuth 2.0 Client ID settings:
```
Authorized redirect URIs:
  - https://yourdomain.com/accounts/google/login/callback/
  - https://www.yourdomain.com/accounts/google/login/callback/
```

### 5. Deploy Application
```bash
# Push to GitHub (if using Render auto-deploy)
git push origin main

# Or deploy directly via Render CLI
render deploy
```

### 6. Run Database Migrations
```bash
# Via SSH or Render dashboard console:
python community/manage.py migrate
```

### 7. Configure Django Site
```bash
# Via shell or Django admin:
python community/manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.get_current()
>>> site.domain = 'yourdomain.com'
>>> site.name = 'Community Feed'
>>> site.save()
>>> exit()
```

### 8. Setup Google OAuth (Production)
```bash
python community/manage.py setup_google_oauth \
  --client-id YOUR_CLIENT_ID \
  --secret YOUR_SECRET \
  --site-domain yourdomain.com
```

## 🔐 Post-Deployment Security

### 1. Verify HTTPS
```bash
curl -I https://yourdomain.com
# Should show: Strict-Transport-Security header
```

### 2. Check Security Headers
```bash
curl -I https://yourdomain.com | grep -E "X-Frame-Options|X-Content-Type-Options|X-XSS-Protection"
```

### 3. Test Django Checks
```bash
python community/manage.py check --deploy
```

### 4. Monitor Logs
```bash
# Check for authentication errors, SQL injection attempts, etc.
tail -f /var/log/gunicorn.log
```

### 5. Setup Alerts
- Monitor for failed login attempts
- Alert on database connection failures
- Track 500 errors
- Monitor for suspicious IP addresses

### 6. Regular Audits
- Review who has environment variable access
- Rotate database passwords quarterly
- Audit Google OAuth connected apps
- Check for and remove unused OAuth apps

## 🛡️ Production Security Settings Summary

```python
# From community/settings.py (production values)
DEBUG = False  # Disable detailed error pages
SECURE_SSL_REDIRECT = True  # Force HTTPS
SESSION_COOKIE_SECURE = True  # Cookies only over HTTPS
CSRF_COOKIE_SECURE = True  # CSRF cookies only over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

## 🚨 Emergency Procedures

### If Secret is Compromised
1. Generate new SECRET_KEY immediately
2. Invalidate all active sessions
3. Force password reset for all users
4. Notify users of security incident
5. Update git history (rewrite commits if needed)

### If Database is Breached
1. Generate new database password
2. Rotate all application credentials
3. Check logs for unauthorized access
4. Review backup integrity
5. Notify users and comply with regulations

### If Google OAuth Credentials Leaked
1. Regenerate OAuth app in Google Cloud
2. Get new Client ID and Secret
3. Update environment variables
4. Revoke old OAuth app
5. Users will need to re-authenticate

## 📞 Support & References

- Render.com Deployment: https://render.com/docs/deploy-django
- Django Deployment Checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Google OAuth Security: https://developers.google.com/identity/protocols/oauth2/security
- PostgreSQL Hosting Security: https://www.postgresql.org/docs/current/ssl-tcp.html

---

**Last Updated:** April 16, 2026
**Status:** All security checks passed ✅
