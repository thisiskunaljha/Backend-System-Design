#!/bin/bash
# Quick setup script for Community Feed

set -e

echo "🚀 Community Feed - Quick Setup"
echo "================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✓ .env file found"
else
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ Created .env - please edit it with your credentials"
    echo ""
    echo "📝 Steps:"
    echo "  1. Edit .env with your Google OAuth credentials"
    echo "  2. Get them from: https://console.cloud.google.com/apis/credentials"
    echo "  3. Then run this script again"
    echo ""
    exit 1
fi

# Source the .env file
export $(grep -v '^#' .env | xargs)

# Check required variables
if [ -z "$SOCIAL_AUTH_GOOGLE_CLIENT_ID" ] || [ "$SOCIAL_AUTH_GOOGLE_CLIENT_ID" = "YOUR_GOOGLE_CLIENT_ID_HERE" ]; then
    echo "❌ Error: SOCIAL_AUTH_GOOGLE_CLIENT_ID not set in .env"
    echo "   Please edit .env and add your Google OAuth Client ID"
    exit 1
fi

if [ -z "$SOCIAL_AUTH_GOOGLE_SECRET" ] || [ "$SOCIAL_AUTH_GOOGLE_SECRET" = "YOUR_GOOGLE_CLIENT_SECRET_HERE" ]; then
    echo "❌ Error: SOCIAL_AUTH_GOOGLE_SECRET not set in .env"
    echo "   Please edit .env and add your Google OAuth Client Secret"
    exit 1
fi

echo "✓ Environment variables loaded"
echo ""

# Change to Django project directory
cd community

echo "📦 Applying migrations..."
python manage.py migrate

echo "✓ Migrations applied"
echo ""

echo "🔐 Configuring Google OAuth..."
python manage.py setup_google_oauth --client-id "$SOCIAL_AUTH_GOOGLE_CLIENT_ID" --secret "$SOCIAL_AUTH_GOOGLE_SECRET"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the development server:"
echo "   cd community && python manage.py runserver"
echo ""
echo "🌐 Access the app at: http://127.0.0.1:8000"
echo ""
