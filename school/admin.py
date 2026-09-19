from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import (
    CustomUser, SchoolSetting, Student, Course, Attendance, Grade,
    Teacher, Classroom, Timetable, SubjectAssignment, FeeStructure,
    Payment, Parent
)

User = get_user_model()


# --- System Setting Admin ---

@admin.register(SchoolSetting)
class SchoolSettingAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'current_session', 'current_term', 'contact_email')

    def has_add_permission(self, request):
        # Prevents creating more than one setting instance in the backend
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevents accidental deletion of the core settings object
        return False


# --- User Management Admins ---

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Options', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Profile Options', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(CustomUser, CustomUserAdmin)


# --- Core Entity Admins ---

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'staff_id', 'department', 'email', 'phone', 'date_joined')
    search_fields = ('full_name', 'staff_id', 'email', 'department')
    list_filter = ('department', 'date_joined')


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    search_fields = ('name',)
    list_filter = ('teacher',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'classroom', 'department', 'email', 'date_registered')
    search_fields = ('name', 'email')
    list_filter = ('classroom', 'department', 'date_registered')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'user')
    search_fields = ('full_name', 'phone')
    filter_horizontal = ('student',)  # Provides an easy UI box for selecting multiple students


# --- Academic Admins ---

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department')
    search_fields = ('code', 'name', 'department')
    list_filter = ('department',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'date')
    list_filter = ('status', 'date', 'student__classroom')
    search_fields = ('student__name',)
    date_hierarchy = 'date'


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'score', 'letter_grade', 'date_recorded')
    list_filter = ('course', 'date_recorded')
    search_fields = ('student__name', 'course__name')


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'day', 'period', 'subject', 'teacher')
    list_filter = ('classroom', 'day', 'period')
    search_fields = ('classroom__name', 'subject__name', 'teacher__full_name')


@admin.register(SubjectAssignment)
class SubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'subject', 'teacher')
    list_filter = ('classroom', 'teacher')
    search_fields = ('classroom__name', 'subject__name', 'teacher__full_name')


# --- Finance Admins ---

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'term', 'session', 'amount')
    list_filter = ('term', 'session', 'classroom')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'term', 'session', 'reference', 'date_paid')
    list_filter = ('term', 'session', 'date_paid')
    search_fields = ('student__name', 'reference')
    date_hierarchy = 'date_paid'