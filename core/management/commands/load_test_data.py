from django.core.management.base import BaseCommand
from django.core.management import call_command
from accounts.models import User
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads all test data into the database and resets test user passwords'

    def handle(self, *args, **kwargs):
        fixture_files = [
            'accounts/fixtures/test_users.json',
            'machinery/fixtures/test_machinery.json',
            'machinery/fixtures/test_collections.json',
            'machinery/fixtures/test_machinery_collections.json',
            'machinery/fixtures/test_machinery_assignments.json',
            'repairs/fixtures/test_warnings.json',
            'repairs/fixtures/test_fault_cases.json',
            'repairs/fixtures/test_fault_notes.json',
        ]
        
        # Load all fixtures
        for fixture in fixture_files:
            self.stdout.write(f'Loading {fixture}...')
            try:
                call_command('loaddata', fixture)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to load {fixture}: {e}'))
        
        # Reset passwords for all test users
        self.reset_test_user_passwords()
    
    def reset_test_user_passwords(self):
        """Reset passwords for all test users to 'password123'"""
        self.stdout.write('\nResetting passwords for test users...')
        
        # Extract usernames from the test_users.json fixture
        user_fixture_path = os.path.join(settings.BASE_DIR, 'accounts/fixtures/test_users.json')
        DEFAULT_PASSWORD = 'password123'
        try:
            with open(user_fixture_path, 'r') as f:
                user_data = json.load(f)
                
            # Extract usernames from the fixture data
            usernames = []
            for user in user_data:
                if user.get('model') == 'accounts.user' and 'fields' in user and 'username' in user['fields']:
                    username = user['fields']['username']
                    usernames.append(username)
            
            if not usernames:
                self.stdout.write(self.style.WARNING('No users found in fixture file'))
                return
                
            self.stdout.write(f'Found {len(usernames)} users in fixture file: {", ".join(usernames)}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error parsing user fixture file: {e}'))
        
        success_count = 0
        fail_count = 0
        
        for username in usernames:
            try:
                # Get the user
                user = User.objects.get(username=username)
                
                # Reset the password
                user.set_password(DEFAULT_PASSWORD)
                user.save()
                
                self.stdout.write(self.style.SUCCESS(f'✅ Reset password for {username} ({user.role})'))
                success_count += 1
                
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'❌ User "{username}" not found'))
                fail_count += 1
        
        # Summary
        self.stdout.write('\n=== Password Reset Summary ===')
        self.stdout.write(self.style.SUCCESS(f'Successfully reset {success_count} user passwords'))
        if fail_count > 0:
            self.stdout.write(self.style.WARNING(f'Failed to find {fail_count} users'))
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f'\nYou can now log in with any of these users with password "{DEFAULT_PASSWORD}"')) 