# Community Feed

## Google Login (via django-allauth)

### 1. Install dependencies

- Ensure these are installed:
  - `django-allauth`
  - `requests`
  - `cryptography`

Example:

```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

### 2. Configure Google OAuth credentials

1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID (Web application)
3. Add authorized redirect URI:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `https://<your-domain>/accounts/google/login/callback/`
4. Copy `CLIENT_ID` and `CLIENT_SECRET`

### 3. Set environment variables

```bash
export SOCIAL_AUTH_GOOGLE_CLIENT_ID='<your-client-id>'
export SOCIAL_AUTH_GOOGLE_SECRET='<your-client-secret>'
```

### 4. Create the SocialApp in Django Admin

- Open `/admin/` and login as superuser.
- Under Social Accounts, add a new Social App:
  - Provider: Google
  - Name: Google
  - Client id: `<your-client-id>`
  - Secret key: `<your-client-secret>`
  - Sites: choose your current site (e.g., `example.com` or `localhost`).

### 5. Run migrations and server

```bash
python3 manage.py migrate
python3 manage.py runserver
```

### 6. Use in UI

- Go to `/login/` for local login
- Go to `/accounts/login/` for allauth login with Google
- Google button will send users to Google OAuth sign-in

