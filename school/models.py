from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# --- System & Dynamic Config Models ---

class SchoolSetting(models.Model):
    """Allows the admin to dynamically control site parameters from the backend."""
    school_name = models.CharField(max_length=250, default="Pintle Solutions")
    slogan = models.CharField(max_length=250, default="Excellence in Education", blank=True)
    current_session = models.CharField(max_length=20, default="2025/2026")
    current_term = models.CharField(max_length=20, default="First Term")
    dashboard_bg = models.ImageField(upload_to='dashboard_bg/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "School Setting"
        verbose_name_plural = "School Settings"

    def save(self, *args, **kwargs):
        # Enforces a single configuration instance in the database
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.school_name


# --- Core User Models ---

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    full_name = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    date_joined = models.DateField()

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Classroom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='student_profile'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    date_registered = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    student = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return self.full_name


# --- Academic Models ---

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Excused', 'Excused'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

    @property
    def letter_grade(self):
        if self.score >= 70:
            return "A"
        elif self.score >= 60:
            return "B"
        elif self.score >= 50:
            return "C"
        elif self.score >= 45:
            return "D"
        elif self.score >= 40:
            return "E"
        return "F"

    class Meta:
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.student.name} - {self.course.name}: {self.score}"


class Timetable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    PERIOD_CHOICES = [
        ('1st Period', '1st Period'),
        ('2nd Period', '2nd Period'),
        ('3rd Period', '3rd Period'),
        ('4th Period', '4th Period'),
        ('5th Period', '5th Period'),
        ('6th Period', '6th Period'),
    ]
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        # Prevents double-booking a classroom at the same day/time slot
        unique_together = ('classroom', 'day', 'period')

    def __str__(self):
        return f"{self.classroom.name} | {self.day} {self.period}"


class SubjectAssignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subject_assignments')

    class Meta:
        unique_together = ('classroom', 'subject')

    def __str__(self):
        return f"{self.classroom.name} - {self.subject.name} → {self.teacher.full_name}"


# --- Finance Models ---

class FeeStructure(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='fee_structures')
    term = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('classroom', 'term', 'session')

    def __str__(self):
        return f"{self.classroom.name} - {self.term} {self.session} ({self.amount})"


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    term = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True, db_index=True)
    reference = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['-date_paid']

    def __str__(self):
        return f"{self.student.name} paid {self.amount_paid}"