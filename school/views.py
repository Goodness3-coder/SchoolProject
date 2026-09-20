from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.db.models import Count, Avg, Sum
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework import generics

from .models import (
    Parent, Student, Course, Attendance, Grade, Teacher, Classroom,
    Timetable, SubjectAssignment, FeeStructure, Payment, CustomUser, SchoolSetting, 
)
from .forms import (
    StudentForm, CourseForm, AttendanceForm, GradeForm, TeacherForm,
    ClassroomForm, TimetableForm, SubjectAssignmentForm, FeeStructureForm, PaymentForm, SchoolSettingForm
)
from .serializers import (
    StudentSerializer, CourseSerializer, GradeSerializer, AttendanceSerializer,
    TeacherSerializer, ClassroomSerializer, TimetableSerializer, SubjectAssignmentSerializer,
    FeeSerializer, PaymentSerializer, ParentSerializer
)
from .permissions import IsAdmin, IsTeacher, IsStudent, IsParent, IsAdminOrTeacher, IsAdminOrTeacherOrParent


# ===================== DASHBOARDS =====================

from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from .models import (
    SchoolSetting, Student, Teacher, Course, Classroom,
    Attendance, Payment, Timetable, SubjectAssignment, Parent, Grade
)


@login_required
def dashboard(request):
    """Main landing dashboard that directs users based on role."""
    return role_based_dashboard(request)


@login_required
def role_based_dashboard(request):
    user_role = str(getattr(request.user, 'role', '') or '').strip().lower()

    # ---------------------------------------------------------
    # 1. STUDENTS & PARENTS (Direct Routing - No Staff/Admin Checks)
    # ---------------------------------------------------------
    if user_role == 'student':
        return redirect('student_dashboard')
    
    if user_role == 'parent':
        return redirect('parent_dashboard')

    # ---------------------------------------------------------
    # 2. OFFICIAL STAFF & ADMIN (Teachers & Superusers)
    # ---------------------------------------------------------
    if user_role == 'teacher':
        return redirect('teacher_dashboard')

    if request.user.is_superuser or request.user.is_staff or user_role in ['admin', 'administrator']:
        return redirect('admin_dashboard')

    # Safe Fallback if a user has no assigned role
    return render(request, 'school/no_role.html', {
        'message': f'Welcome {request.user.username}! Your account is active, but no role has been assigned yet. Please contact an administrator.'
    })


@login_required
def student_dashboard(request):
    user_role = str(getattr(request.user, 'role', '') or '').strip().lower()

    if user_role != "student" and not request.user.is_superuser:
        messages.warning(request, "Unauthorized access.")
        return redirect('role_based_dashboard')

    student = Student.objects.filter(user=request.user).first()
    if not student:
        if request.user.is_superuser:
            messages.info(request, "Superusers do not have an associated Student record.")
            return redirect('admin_dashboard')
        messages.error(request, "Student profile details not found. Please contact an administrator.")
        return redirect('role_based_dashboard')

    grades = Grade.objects.filter(student=student)
    attendance_records = Attendance.objects.filter(student=student)
    timetable = Timetable.objects.filter(classroom=student.classroom) if student.classroom else []

    return render(request, 'school/student_dashboard.html', {
        'student': student,
        'grades': grades,
        'attendance_records': attendance_records,
        'timetable': timetable,
    })


@login_required
def parent_dashboard(request):
    user_role = str(getattr(request.user, 'role', '') or '').strip().lower()

    if user_role != "parent" and not request.user.is_superuser:
        messages.warning(request, "Unauthorized access.")
        return redirect('role_based_dashboard')

    parent = Parent.objects.filter(user=request.user).first()
    if not parent:
        if request.user.is_superuser:
            messages.info(request, "Superusers do not have an associated Parent record.")
            return redirect('admin_dashboard')
        messages.error(request, "Parent profile details not found. Please contact an administrator.")
        return redirect('role_based_dashboard')

    students = parent.student.all() if hasattr(parent, 'student') else []

    student_data = []
    for st in students:
        timetable = Timetable.objects.filter(classroom=st.classroom) if st.classroom else []
        assignments = SubjectAssignment.objects.filter(classroom=st.classroom) if st.classroom else []
        payments = Payment.objects.filter(student=st)
        student_data.append({
            'student': st,
            'timetable': timetable,
            'assignments': assignments,
            'payments': payments,
        })

    return render(request, 'school/parent_dashboard.html', {
        'parent': parent,
        'student_data': student_data,
    })


@login_required
def teacher_dashboard(request):
    user_role = str(getattr(request.user, 'role', '') or '').strip().lower()
    
    if user_role != "teacher" and not request.user.is_superuser:
        messages.warning(request, "Unauthorized access.")
        return redirect('role_based_dashboard')

    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        if request.user.is_superuser:
            messages.info(request, "Superusers do not have an associated Teacher record.")
            return redirect('admin_dashboard')
        messages.error(request, "Teacher profile details not found. Please contact an administrator.")
        return redirect('role_based_dashboard')

    assignments = SubjectAssignment.objects.filter(teacher=teacher)
    classrooms = assignments.values_list('classroom', flat=True).distinct()
    timetable_entries = Timetable.objects.filter(classroom__in=classrooms)
    students = Student.objects.filter(classroom__in=classrooms)

    return render(request, 'school/teacher_dashboard.html', {
        'teacher': teacher,
        'assignments': assignments,
        'timetable_entries': timetable_entries,
        'students': students,
    })


@login_required
def admin_dashboard(request):
    user_role = str(getattr(request.user, 'role', '')).strip().lower()
    is_admin_user = request.user.is_staff or request.user.is_superuser or user_role in ['admin', 'administrator']

    if not is_admin_user:
        messages.error(request, "Access denied. You do not have permission to view the Admin Dashboard.")
        return redirect('role_based_dashboard')

    school_setting = SchoolSetting.objects.first()

    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_classrooms = Classroom.objects.count()
    total_attendance = Attendance.objects.count()
    present_today = Attendance.objects.filter(date=date.today(), status="Present").count()
    total_revenue = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0.00

    classrooms = Classroom.objects.all()
    class_id = request.GET.get('classroom')
    timetable_entries = Timetable.objects.all()
    if class_id:
        timetable_entries = timetable_entries.filter(classroom_id=class_id)

    class_data = Classroom.objects.annotate(student_count=Count('students')).values_list('name', 'student_count')
    class_labels = [c[0] for c in class_data]
    student_counts = [c[1] for c in class_data]

    subject_data = Course.objects.annotate(avg_score=Avg('grades__score')).values_list('name', 'avg_score')
    subject_labels = [s[0] for s in subject_data]
    avg_scores = [round(s[1] or 0, 2) for s in subject_data]

    context = {
        'school_setting': school_setting,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_classrooms': total_classrooms,
        'total_attendance': total_attendance,
        'present_today': present_today,
        'total_revenue': total_revenue,
        'classrooms': classrooms,
        'timetable_entries': timetable_entries,
        'selected_classroom': int(class_id) if class_id and class_id.isdigit() else None,
        'class_labels': class_labels,
        'student_counts': student_counts,
        'subject_labels': subject_labels,
        'avg_scores': avg_scores,
    }
    return render(request, 'school/admin_dashboard.html', context)


@login_required
def stats_dashboard(request):
    """Alias view for admin stats dashboard analytics."""
    return admin_dashboard(request)

# ===================== AUTHENTICATION =====================



def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('role_based_dashboard')  # FIXED: Redirect instead of direct function call
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "school/login.html")


def login_view(request):
    """Standard Django login fallback view."""
    return user_login(request)


def user_logout(request):
    logout(request)
    return redirect('login')


def parent_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            parent_group, _ = Group.objects.get_or_create(name='Parent')
            user.groups.add(parent_group)
            messages.success(request, "Parent account created successfully! Please login.")
            return redirect('parent_login')
    else:
        form = UserCreationForm()
    return render(request, 'school/parent_register.html', {'form': form})


def parent_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('role_based_dashboard')  # FIXED: Route through role_based_dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'school/parent_login.html', {'form': form})


def parent_logout(request):
    logout(request)
    return redirect('parent_login')


def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        # Check user validity (using role check or active status)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('role_based_dashboard')  # FIXED: Route through role_based_dashboard
        else:
            return render(request, 'school/student_login.html', {"error": "Invalid credentials"})
            
    return render(request, 'school/student_login.html')


# ===================== STUDENT MANAGEMENT =====================

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'school/students_list.html', {'students': students})


@login_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'school/student_form.html', {'form': form})


@login_required
def add_student(request):
    """Alias function for student creation."""
    return student_create(request)


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'school/student_form.html', {'form': form})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'school/student_confirm_delete.html', {'student': student})


@login_required
def student_report(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    grades = Grade.objects.filter(student=student).select_related('course')
    total_present = Attendance.objects.filter(student=student, status='Present').count()
    total_absent = Attendance.objects.filter(student=student, status='Absent').count()

    return render(request, 'school/student_report.html', {
        'student': student,
        'grades': grades,
        'total_present': total_present,
        'total_absent': total_absent,
    })


@login_required
def student_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    grades = Grade.objects.filter(student=student).select_related('course')
    total_score = sum(g.score for g in grades)
    average_score = total_score / grades.count() if grades.exists() else 0
    return render(request, 'school/report_card.html', {
        'student': student,
        'grades': grades,
        'total': total_score,
        'average': round(average_score, 2)
    })


# ===================== TEACHER MANAGEMENT =====================

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'school/teachers_list.html', {'teachers': teachers})


@login_required
def teacher_create(request):
    form = TeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('teacher_list')
    return render(request, 'school/teacher_form.html', {'form': form})


@login_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, instance=teacher)
    if form.is_valid():
        form.save()
        return redirect('teacher_list')
    return render(request, 'school/teacher_form.html', {'form': form})


@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'school/teacher_confirm_delete.html', {'teacher': teacher})


# ===================== COURSE MANAGEMENT =====================

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'school/courses_list.html', {'courses': courses})


@login_required
def course_create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('course_list')
    return render(request, 'school/course_form.html', {'form': form})


@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect('course_list')
    return render(request, 'school/course_form.html', {'form': form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'school/course_confirm_delete.html', {'course': course})


# ===================== CLASSROOM MANAGEMENT =====================

@login_required
def classroom_list(request):
    classrooms = Classroom.objects.select_related('teacher').all()
    return render(request, 'school/classrooms_list.html', {'classrooms': classrooms})


@login_required
def classroom_create(request):
    form = ClassroomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('classroom_list')
    return render(request, 'school/classroom_form.html', {'form': form})


@login_required
def classroom_update(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    form = ClassroomForm(request.POST or None, instance=classroom)
    if form.is_valid():
        form.save()
        return redirect('classroom_list')
    return render(request, 'school/classroom_form.html', {'form': form})


@login_required
def classroom_delete(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        classroom.delete()
        return redirect('classroom_list')
    return render(request, 'school/classroom_confirm_delete.html', {'classroom': classroom})


# ===================== ATTENDANCE MANAGEMENT =====================

@login_required
def attendance_list(request):
    attendance_records = Attendance.objects.select_related('student').order_by('-date')
    return render(request, 'school/attendance_list.html', {'attendance_records': attendance_records})


@login_required
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('attendance_list')
    return render(request, 'school/attendance_form.html', {'form': form})


@login_required
def attendance_update(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    form = AttendanceForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('attendance_list')
    return render(request, 'school/attendance_form.html', {'form': form})


@login_required
def attendance_delete(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('attendance_list')
    return render(request, 'school/attendance_confirm_delete.html', {'record': record})


# ===================== GRADE MANAGEMENT =====================

@login_required
def grade_list(request):
    grades = Grade.objects.select_related('student', 'course').all()
    return render(request, 'school/grades_list.html', {'grades': grades})


@login_required
def grade_create(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('grade_list')
    return render(request, 'school/grade_form.html', {'form': form})


@login_required
def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    form = GradeForm(request.POST or None, instance=grade)
    if form.is_valid():
        form.save()
        return redirect('grade_list')
    return render(request, 'school/grade_form.html', {'form': form})


@login_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grade_list')
    return render(request, 'school/grade_confirm_delete.html', {'grade': grade})


# ===================== TIMETABLE =====================

@login_required
def timetable_list(request):
    user_role = getattr(request.user, 'role', '').lower()
    class_id = request.GET.get('classroom')
    classrooms = Classroom.objects.all()

    if user_role == "admin" or request.user.is_superuser:
        timetable_entries = Timetable.objects.all()
    elif user_role == "teacher":
        teacher = get_object_or_404(Teacher, user=request.user)
        assigned_classrooms = SubjectAssignment.objects.filter(teacher=teacher).values_list('classroom', flat=True)
        timetable_entries = Timetable.objects.filter(classroom__in=assigned_classrooms)
    elif user_role == "student":
        student = get_object_or_404(Student, user=request.user)
        timetable_entries = Timetable.objects.filter(classroom=student.classroom)
    elif user_role == "parent":
        parent = get_object_or_404(Parent, user=request.user)
        children_classrooms = parent.student.all().values_list('classroom', flat=True)
        timetable_entries = Timetable.objects.filter(classroom__in=children_classrooms)
    else:
        messages.warning(request, "Unauthorized access.")
        return redirect('role_based_dashboard')

    if class_id:
        timetable_entries = timetable_entries.filter(classroom_id=class_id)

    return render(request, 'school/timetable_list.html', {
        'classrooms': classrooms,
        'timetable_entries': timetable_entries,
        'selected_classroom': int(class_id) if class_id else None
    })


@login_required
def timetable_create(request):
    user_role = getattr(request.user, 'role', '').lower()
    if user_role not in ['admin', 'teacher'] and not request.user.is_superuser:
        messages.warning(request, "Unauthorized access.")
        return redirect('timetable_list')

    form = TimetableForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('timetable_list')

    return render(request, 'school/timetable_form.html', {'form': form})


@login_required
def timetable_delete(request, pk):
    user_role = getattr(request.user, 'role', '').lower()
    if user_role not in ['admin', 'teacher'] and not request.user.is_superuser:
        messages.warning(request, "Unauthorized access.")
        return redirect('timetable_list')

    entry = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('timetable_list')

    return render(request, 'school/timetable_confirm_delete.html', {'entry': entry})


# ===================== ASSIGNMENT MANAGEMENT =====================

@login_required
def assignment_list(request):
    assignments = SubjectAssignment.objects.select_related('classroom', 'subject', 'teacher')
    return render(request, 'school/assignments_list.html', {'assignments': assignments})


@login_required
def assignment_create(request):
    form = SubjectAssignmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('assignment_list')
    return render(request, 'school/assignment_form.html', {'form': form})


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(SubjectAssignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')
    return render(request, 'school/assignment_confirm_delete.html', {'assignment': assignment})


# ===================== FEES & PAYMENTS =====================

@login_required
def fee_structure_list(request):
    fees = FeeStructure.objects.select_related('classroom')
    return render(request, 'school/fee_structure_list.html', {'fees': fees})


@login_required
def fee_structure_create(request):
    form = FeeStructureForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('fee_structure_list')
    return render(request, 'school/fee_structure_form.html', {'form': form})


@login_required
def payment_list(request):
    payments = Payment.objects.select_related('student')
    return render(request, 'school/payment_list.html', {'payments': payments})


@login_required
def payment_create(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payment_list')
    return render(request, 'school/payment_form.html', {'form': form})


@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    form = PaymentForm(request.POST or None, instance=payment)
    if form.is_valid():
        form.save()
        return redirect('payment_list')
    return render(request, 'school/payment_form.html', {'form': form})


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        payment.delete()
        return redirect('payment_list')
    return render(request, 'school/payment_confirm_delete.html', {'payment': payment})


# ===================== DRF API VIEWS =====================

class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrTeacher()]
        elif self.request.method == "POST":
            return [IsAdmin()]
        return [IsAdmin()]


class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [IsAdminOrTeacher()]


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrTeacher]


class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrTeacher]


class GradeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrTeacher]


class GradeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrTeacher]


class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTeacher]


class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTeacher]


class TeacherListCreateAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]


class TeacherRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]


class ClassroomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdminOrTeacher]


class ClassroomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdminOrTeacher]


class TimetableListCreateAPIView(generics.ListCreateAPIView):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdminOrTeacher]


class TimetableRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdminOrTeacher]


class SubjectAssignmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubjectAssignment.objects.all()
    serializer_class = SubjectAssignmentSerializer
    permission_classes = [IsAdminOrTeacher]


class SubjectAssignmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubjectAssignment.objects.all()
    serializer_class = SubjectAssignmentSerializer
    permission_classes = [IsAdminOrTeacher]


class FeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [IsAdmin]


class FeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [IsAdmin]


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrTeacher(), IsParent()]
        elif self.request.method == "POST":
            return [IsAdmin()]
        return [IsAdmin()]


class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdmin]


class ParentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAdmin]


class ParentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAdmin]


class StudentOwnGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Grade.objects.filter(student__user=self.request.user)


class StudentOwnAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Attendance.objects.filter(student__user=self.request.user)


class ParentChildGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return Grade.objects.filter(student__parent=self.request.user)


class ParentChildAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return Attendance.objects.filter(student__parent=self.request.user)
    

def get_or_create_school_setting():
    """Helper to ensure a single SchoolSetting record always exists."""
    setting = SchoolSetting.objects.first()
    if not setting:
        setting = SchoolSetting.objects.create(
            school_name="Default School Name",
            slogan="Knowledge is Power",
            current_session="2025/2026",
            current_term="First Term",
            contact_email="admin@school.com",
            contact_phone="+234 800 000 0000"
        )
    return setting

@login_required
def edit_school_settings(request):
    """View allowing admins to update school settings & background image."""
    setting = get_or_create_school_setting()

    if request.method == 'POST':
        form = SchoolSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SchoolSettingForm(instance=setting)

    return render(request, 'school/edit_settings.html', {'form': form})

@login_required
def role_based_dashboard(request):
    # Safely get role string in lowercase
    user_role = getattr(request.user, 'role', '').lower()
    
    # Superusers always get admin access
    if request.user.is_superuser or user_role in ['admin', 'administrator']:
        return redirect('admin_dashboard')
    elif user_role == 'teacher':
        return redirect('teacher_dashboard')
    elif user_role == 'student':
        return redirect('student_dashboard')
    elif user_role == 'parent':
        return redirect('parent_dashboard')
    else:
        # Fallback if role is not set
        return redirect('admin_dashboard')