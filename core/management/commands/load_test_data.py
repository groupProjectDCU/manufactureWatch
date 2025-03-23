from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Loads all test data into the database'

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
        
        for fixture in fixture_files:
            self.stdout.write(f'Loading {fixture}...')
            try:
                call_command('loaddata', fixture)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to load {fixture}: {e}')) 