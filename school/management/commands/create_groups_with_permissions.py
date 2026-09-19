from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from school.models import Student, Grade, Attendance, Course, Payment

class Command(BaseCommand):
    help = 'Create Admin, Teacher, Parent groups with appropriate permissions'

    def handle(self, *args, **kwargs):
        # === 1. Admin Group ===
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write('✅ Created group: Admin')
        else:
            self.stdout.write('⚠️ Admin group already exists')
        # All permissions
        admin_perms = Permission.objects.all()
        admin_group.permissions.set(admin_perms)

        # === 2. Teacher Group ===
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        if created:
            self.stdout.write('✅ Created group: Teacher')
        else:
            self.stdout.write('⚠️ Teacher group already exists')

        teacher_perms = Permission.objects.filter(
            content_type__model__in=['grade', 'attendance', 'course']
        )
        teacher_group.permissions.set(teacher_perms)

        # === 3. Parent Group ===
        parent_group, created = Group.objects.get_or_create(name='Parent')
        if created:
            self.stdout.write('✅ Created group: Parent')
        else:
            self.stdout.write('⚠️ Parent group already exists')

        parent_perms = Permission.objects.filter(
            content_type__model__in=['student', 'payment']
        ).filter(codename__startswith='view_')
        parent_group.permissions.set(parent_perms)

        self.stdout.write(self.style.SUCCESS('🎉 Groups and permissions set up successfully.'))
