# Google OAuth Setup Guide

This guide explains how to enable Google login for your Community Feed application.

## Quick Setup (Recommended)

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth client ID**
5. Choose **Web application** as the application type
6. Add these **Authorized redirect URIs**:
   - `http://localhost:8000/accounts/google/login/callback/` (for development)
   - `http://127.0.0.1:8000/accounts/google/login/callback/` (alternative localhost)
   - `https://yourdomain.com/accounts/google/login/callback/` (for production)
7. Copy your **Client ID** and **Client Secret**

### Step 2: Configure Django with Google OAuth

Run the automated setup command:

```bash
# Interactive mode (prompts for credentials)
python manage.py setup_google_oauth

# Or with command line arguments
python manage.py setup_google_oauth \
  --client-id YOUR_CLIENT_ID \
  --secret YOUR_CLIENT_SECRET \
  --site-domain yourdomain.com
```

### Step 3: Test Google Login

1. Start your development server:
   ```bash
   python manage.py runserver
   ```

2. Go to http://localhost:8000/login/

3. Click "✓ Continue with Google"

4. You'll be redirected to Google's login page

5. After authenticating, you'll be redirected back to your application

## Manual Setup (Alternative)

If you prefer to set up via Django Admin:

1. Run migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Go to `http://localhost:8000/admin/`

4. Navigate to **Sites** and set your domain:
   - Domain: `localhost:8000` (or your domain)
   - Display Name: `Community Feed`

5. Go to **Social Applications** → **Add Social Application**:
   - Provider: `Google`
   - Name: `Google`
   - Client ID: `<your-client-id>`
   - Secret Key: `<your-client-secret>`
   - Sites: Select your site
   - Save

## Environment Variables (Optional)

For production, you can also store credentials as environment variables:

```bash
# In .env or Heroku/Render environment settings
SOCIAL_AUTH_GOOGLE_CLIENT_ID=your_client_id
SOCIAL_AUTH_GOOGLE_SECRET=your_client_secret
```

Then update your settings.py to use them:
```python
# In settings.py
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'CLIENT_ID': os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID'),
        'SECRET': os.environ.get('SOCIAL_AUTH_GOOGLE_SECRET'),
    }
}
```

## Deployment Setup

### For Render.com

1. Go to your project dashboard
2. Add environment variables:
   - `SOCIAL_AUTH_GOOGLE_CLIENT_ID=your-client-id`
   - `SOCIAL_AUTH_GOOGLE_SECRET=your-client-secret`
3. Update authorized redirect URI in Google Cloud:
   - `https://your-app.onrender.com/accounts/google/login/callback/`
4. Run the setup command on the deployed server:
   ```bash
   python manage.py setup_google_oauth --client-id ... --secret ...
   ```

### For Heroku

```bash
# Add environment variables
heroku config:set SOCIAL_AUTH_GOOGLE_CLIENT_ID=your-client-id
heroku config:set SOCIAL_AUTH_GOOGLE_SECRET=your-client-secret

# Then run the setup command
heroku run python manage.py setup_google_oauth --client-id ... --secret ...
```

## Troubleshooting

### "Redirect URI mismatch" Error

This means the callback URL in Google Cloud Console doesn't match your app's domain.

**Solution:**
1. Check your current domain: Go to `http://localhost:8000/admin/sites/`
2. Update Google Cloud Console with the correct authorized redirect URI
3. Ensure the Site in Django Admin matches your domain

### "No Site was found" Error

This means the Site configuration is missing.

**Solution:**
Run:
```bash
python manage.py setup_google_oauth --site-domain your-domain
```

### Google Login Button Not Showing

Make sure the template is loading the socialaccount template tags:
```django
{% load socialaccount %}
```

## API Integration

If you're using the REST API, here's how to set up Google login:

### For Web Apps (Frontend JavaScript)

```javascript
// After Google redirects user back to your app
const response = await fetch('/accounts/google/login/callback/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: authorizationCode // From Google OAuth flow
  })
});
```

### For Mobile Apps

Use the OAuth 2.0 flow directly with Google and send the ID token to your backend:

```python
# Endpoint to validate token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.auth.transport import requests
from google.oauth2 import id_token

@api_view(['POST'])
def google_auth(request):
    token = request.data.get('token')
    try:
        # Verify token with Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        # Create or get user
        # Return auth token
    except ValueError:
        return Response({'error': 'Invalid token'}, status=400)
```

## Next Steps

1. ✅ Google login is now configured
2. Test the login flow
3. Customize the user profile creation (optional)
4. Add Google login to other pages (optional)

## Support

For issues, check:
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
