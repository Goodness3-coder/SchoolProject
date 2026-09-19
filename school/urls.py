from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ===================== DASHBOARD =====================
    # Dynamic central router dashboard
    path('dashboard/', views.role_based_dashboard, name='dashboard'),
    path('dashboard/router/', views.role_based_dashboard, name='role_based_dashboard'),
    
    # Specific Role Dashboards
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),

    # ===================== SCHOOL SETTINGS =====================
    path('settings/edit/', views.edit_school_settings, name='edit_school_settings'),

    # ===================== STUDENTS =====================
    path('', views.student_list, name='student_list'),
    path('student/add/', views.student_create, name='student_create'),
    path('student/<int:pk>/edit/', views.student_update, name='student_update'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/<int:student_id>/report/', views.student_report, name='student_report'),
    path('students/<int:student_id>/report-card/', views.student_report_card, name='student_report_card'),
    path('student/login/', views.student_login, name='student_login'),

    # ===================== COURSES =====================
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # ===================== ATTENDANCE =====================
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/edit/', views.attendance_update, name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),

    # ===================== GRADES =====================
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/add/', views.grade_create, name='grade_create'),
    path('grades/<int:pk>/edit/', views.grade_update, name='grade_update'),
    path('grades/<int:pk>/delete/', views.grade_delete, name='grade_delete'),

    # ==================== AUTH ====================
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # ==================== TEACHERS ====================
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    # ==================== CLASSROOMS ====================
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('classrooms/add/', views.classroom_create, name='classroom_create'),
    path('classrooms/<int:pk>/edit/', views.classroom_update, name='classroom_update'),
    path('classrooms/<int:pk>/delete/', views.classroom_delete, name='classroom_delete'),

    # ==================== TIMETABLE ====================
    path('timetable/', views.timetable_list, name='timetable_list'),
    path('timetable/add/', views.timetable_create, name='timetable_create'),
    path('timetable/<int:pk>/delete/', views.timetable_delete, name='timetable_delete'),

    # ==================== SUBJECT ASSIGNMENT ====================
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/add/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),

    # ==================== FEES & PAYMENTS ====================
    path('fees/', views.fee_structure_list, name='fee_structure_list'),
    path('fees/add/', views.fee_structure_create, name='fee_structure_create'),

    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/edit/', views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),

    # ==================== PARENT LOGIN SYSTEM ====================
    path('parent/register/', views.parent_register, name='parent_register'),
    path('parent/login/', views.parent_login, name='parent_login'),
    path('parent/logout/', views.parent_logout, name='parent_logout'),

    # ==================== DRF API ENDPOINTS ====================
    # ---- STUDENTS API ----
    path('api/students/', views.StudentListCreateAPIView.as_view(), name='api_student_list_create'),
    path('api/students/<int:pk>/', views.StudentRetrieveUpdateDestroyAPIView.as_view(), name='api_student_detail'),

    # ---- COURSES API ----
    path('api/courses/', views.CourseListCreateAPIView.as_view(), name='api_course_list_create'),
    path('api/courses/<int:pk>/', views.CourseRetrieveUpdateDestroyAPIView.as_view(), name='api_course_detail'),

    # ---- GRADES API ----
    path('api/grades/', views.GradeListCreateAPIView.as_view(), name='api_grade_list_create'),
    path('api/grades/<int:pk>/', views.GradeRetrieveUpdateDestroyAPIView.as_view(), name='api_grade_detail'),

    # ---- ATTENDANCE API ----
    path('api/attendance/', views.AttendanceListCreateAPIView.as_view(), name='api_attendance_list_create'),
    path('api/attendance/<int:pk>/', views.AttendanceRetrieveUpdateDestroyAPIView.as_view(), name='api_attendance_detail'),

    # ---- TEACHERS API ----
    path('api/teachers/', views.TeacherListCreateAPIView.as_view(), name='api_teacher_list_create'),
    path('api/teachers/<int:pk>/', views.TeacherRetrieveUpdateDestroyAPIView.as_view(), name='api_teacher_detail'),

    # ---- CLASSROOMS API ----
    path('api/classrooms/', views.ClassroomListCreateAPIView.as_view(), name='api_classroom_list_create'),
    path('api/classrooms/<int:pk>/', views.ClassroomRetrieveUpdateDestroyAPIView.as_view(), name='api_classroom_detail'),

    # ---- TIMETABLE API ----
    path('api/timetable/', views.TimetableListCreateAPIView.as_view(), name='api_timetable_list_create'),
    path('api/timetable/<int:pk>/', views.TimetableRetrieveUpdateDestroyAPIView.as_view(), name='api_timetable_detail'),

    # ---- SUBJECT ASSIGNMENTS API ----
    path('api/assignments/', views.SubjectAssignmentListCreateAPIView.as_view(), name='api_assignment_list_create'),
    path('api/assignments/<int:pk>/', views.SubjectAssignmentRetrieveUpdateDestroyAPIView.as_view(), name='api_assignment_detail'),

    # ---- FEES API ----
    path('api/fees/', views.FeeListCreateAPIView.as_view(), name='api_fee_list_create'),
    path('api/fees/<int:pk>/', views.FeeRetrieveUpdateDestroyAPIView.as_view(), name='api_fee_detail'),

    # ---- PAYMENTS API ----
    path('api/payments/', views.PaymentListCreateAPIView.as_view(), name='api_payment_list_create'),
    path('api/payments/<int:pk>/', views.PaymentRetrieveUpdateDestroyAPIView.as_view(), name='api_payment_detail'),

    # ---- PARENTS API ----
    path('api/parents/', views.ParentListCreateAPIView.as_view(), name='api_parent_list_create'),
    path('api/parents/<int:pk>/', views.ParentRetrieveUpdateDestroyAPIView.as_view(), name='api_parent_detail'),

    # ---- EXTRA: Student & Parent own views ----
    path('api/my/grades/', views.StudentOwnGradesView.as_view(), name='api_student_own_grades'),
    path('api/my/attendance/', views.StudentOwnAttendanceView.as_view(), name='api_student_own_attendance'),
    path('api/parent/grades/', views.ParentChildGradesView.as_view(), name='api_parent_child_grades'),
    path('api/parent/attendance/', views.ParentChildAttendanceView.as_view(), name='api_parent_child_attendance'),
]