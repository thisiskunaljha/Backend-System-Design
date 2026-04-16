"""
Django management command to set up Google OAuth for django-allauth.

Usage:
    python manage.py setup_google_oauth --client-id YOUR_CLIENT_ID --secret YOUR_CLIENT_SECRET
    
Or interactively:
    python manage.py setup_google_oauth
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Set up Google OAuth credentials for django-allauth'

    def add_arguments(self, parser):
        parser.add_argument(
            '--client-id',
            type=str,
            help='Google OAuth Client ID'
        )
        parser.add_argument(
            '--secret',
            type=str,
            help='Google OAuth Client Secret'
        )
        parser.add_argument(
            '--site-domain',
            type=str,
            default='localhost',
            help='Site domain (default: localhost)'
        )
        parser.add_argument(
            '--site-name',
            type=str,
            default='Community Feed',
            help='Site name (default: Community Feed)'
        )

    def handle(self, *args, **options):
        client_id = options.get('client_id')
        secret = options.get('secret')
        site_domain = options.get('site_domain')
        site_name = options.get('site_name')

        # Get credentials from user if not provided
        if not client_id:
            self.stdout.write(
                self.style.WARNING(
                    '\n📋 To set up Google OAuth:\n'
                    '1. Go to: https://console.cloud.google.com/apis/credentials\n'
                    '2. Create OAuth 2.0 Client ID (Web application)\n'
                    '3. Add authorized redirect URIs:\n'
                    f'   - http://localhost:8000/accounts/google/login/callback/\n'
                    f'   - http://{site_domain}/accounts/google/login/callback/\n'
                    '4. Copy your credentials below\n'
                )
            )
            client_id = input('🔑 Enter Google Client ID: ').strip()
            secret = input('🔐 Enter Google Client Secret: ').strip()
            site_domain = input(
                f'🌐 Enter your site domain [{site_domain}]: '
            ).strip() or site_domain

        if not client_id or not secret:
            raise CommandError('Client ID and Secret are required')

        try:
            # Update or create Site
            site, created = Site.objects.get_or_create(
                pk=1,
                defaults={
                    'domain': site_domain,
                    'name': site_name
                }
            )
            if not created:
                site.domain = site_domain
                site.name = site_name
                site.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Site updated: {site.domain}')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Site created: {site.domain}')
                )

            # Create or update Google OAuth app
            google_app, created = SocialApp.objects.get_or_create(
                provider='google',
                defaults={
                    'name': 'Google',
                    'client_id': client_id,
                    'secret': secret,
                }
            )

            if not created:
                google_app.client_id = client_id
                google_app.secret = secret
                google_app.save()
                self.stdout.write(
                    self.style.SUCCESS('✓ Google OAuth updated')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✓ Google OAuth created')
                )

            # Ensure the app is associated with the site
            if site not in google_app.sites.all():
                google_app.sites.add(site)
                self.stdout.write(
                    self.style.SUCCESS('✓ Site associated with Google OAuth')
                )

            self.stdout.write(
                self.style.SUCCESS(
                    '\n✅ Google OAuth setup complete!\n'
                    f'   Domain: {site.domain}\n'
                    f'   Provider: Google\n'
                    f'   Status: Ready\n\n'
                    '🚀 You can now log in with Google at:\n'
                    f'   http://{site.domain}/login/\n'
                )
            )

        except IntegrityError as e:
            raise CommandError(f'Error setting up Google OAuth: {str(e)}')
        except Exception as e:
            raise CommandError(f'Unexpected error: {str(e)}')
