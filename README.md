# Community Feed (Django)

This repository contains a Django project (`community`) with a `feed` app.

## Quick start (local)

1. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update values (optional for local):

```bash
cp .env.example .env
# edit .env to set SECRET_KEY, DEBUG, DATABASE_URL
```

4. Run migrations and start server:

```bash
python community/manage.py migrate
python community/manage.py runserver
```

## Deploying to Render

Use these settings in Render when creating the Web Service:

- Environment: `Python`
- Root Directory: `/` (repository root)
- Build Command: `bash ./build.sh`
- Start Command: `gunicorn --chdir community community.wsgi`
- Python version: set to `3.11` (or as pinned in `runtime.txt`)

Required environment variables in Render:

- `SECRET_KEY` (generate and paste a secure key)
- `DEBUG` (`0` for production)
- `DATABASE_URL` (Render Postgres add-on provides this automatically)

## Notes

- Static files are served with WhiteNoise.
- The repository contains `build.sh` which installs dependencies, runs migrations, and collects static files.
- For local development you can use the `.env.example` file as a starting point.
