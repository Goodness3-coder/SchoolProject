import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates or updates the default superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_PASSWORD', 'Admin12345!')

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        
        user.is_staff = True
        user.is_superuser = True
        
        # Explicitly assign 'ADMIN' role to pass your custom dashboard permission check
        if hasattr(user, 'role'):
            user.role = 'ADMIN'
            
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" updated successfully with ADMIN permissions.'))