from django.urls import path, include
from .views import (
    StudentListCreateAPIView, StudentRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView,
    GradeListCreateAPIView, GradeRetrieveUpdateDestroyAPIView,
    AttendanceListCreateAPIView, AttendanceRetrieveUpdateDestroyAPIView,
    TeacherListCreateAPIView, TeacherRetrieveUpdateDestroyAPIView,
    ClassroomListCreateAPIView, ClassroomRetrieveUpdateDestroyAPIView,
    TimetableListCreateAPIView, TimetableRetrieveUpdateDestroyAPIView,
    SubjectAssignmentListCreateAPIView, SubjectAssignmentRetrieveUpdateDestroyAPIView,
    FeeListCreateAPIView, FeeRetrieveUpdateDestroyAPIView,
    PaymentListCreateAPIView, PaymentRetrieveUpdateDestroyAPIView,
    ParentListCreateAPIView, ParentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # ---- STUDENTS ----
    path("students/", StudentListCreateAPIView.as_view(), name="student_api_list"),
    path("students/<int:pk>/", StudentRetrieveUpdateDestroyAPIView.as_view(), name="student_api_detail"),

    # ---- COURSES ----
    path("courses/", CourseListCreateAPIView.as_view(), name="course_api_list"),
    path("courses/<int:pk>/", CourseRetrieveUpdateDestroyAPIView.as_view(), name="course_api_detail"),

    # ---- GRADES ----
    path("grades/", GradeListCreateAPIView.as_view(), name="grade_api_list"),
    path("grades/<int:pk>/", GradeRetrieveUpdateDestroyAPIView.as_view(), name="grade_api_detail"),

    # ---- ATTENDANCE ----
    path("attendance/", AttendanceListCreateAPIView.as_view(), name="attendance_api_list"),
    path("attendance/<int:pk>/", AttendanceRetrieveUpdateDestroyAPIView.as_view(), name="attendance_api_detail"),

    # ---- TEACHERS ----
    path("teachers/", TeacherListCreateAPIView.as_view(), name="teacher_api_list"),
    path("teachers/<int:pk>/", TeacherRetrieveUpdateDestroyAPIView.as_view(), name="teacher_api_detail"),

    # ---- CLASSROOMS ----
    path("classrooms/", ClassroomListCreateAPIView.as_view(), name="classroom_api_list"),
    path("classrooms/<int:pk>/", ClassroomRetrieveUpdateDestroyAPIView.as_view(), name="classroom_api_detail"),

    # ---- TIMETABLE ----
    path("timetables/", TimetableListCreateAPIView.as_view(), name="timetable_api_list"),
    path("timetables/<int:pk>/", TimetableRetrieveUpdateDestroyAPIView.as_view(), name="timetable_api_detail"),

    # ---- SUBJECT ASSIGNMENTS ----
    path("subject-assignments/", SubjectAssignmentListCreateAPIView.as_view(), name="subject_assignment_api_list"),
    path("subject-assignments/<int:pk>/", SubjectAssignmentRetrieveUpdateDestroyAPIView.as_view(), name="subject_assignment_api_detail"),

    # ---- FEES ----
    path("fees/", FeeListCreateAPIView.as_view(), name="fee_api_list"),
    path("fees/<int:pk>/", FeeRetrieveUpdateDestroyAPIView.as_view(), name="fee_api_detail"),

    # ---- PAYMENTS ----
    path("payments/", PaymentListCreateAPIView.as_view(), name="payment_api_list"),
    path("payments/<int:pk>/", PaymentRetrieveUpdateDestroyAPIView.as_view(), name="payment_api_detail"),

    # ---- PARENTS ----
    path("parents/", ParentListCreateAPIView.as_view(), name="parent_api_list"),
    path("parents/<int:pk>/", ParentRetrieveUpdateDestroyAPIView.as_view(), name="parent_api_detail"),


    path('students/', StudentListCreateAPIView.as_view(), name='student_api_list'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyAPIView.as_view(), name='student_api_detail'),

    # DRF login/logout
    path('auth/', include('rest_framework.urls')),
]


