from rest_framework import serializers
from .models import Student, Course, Grade, Attendance, Teacher, Classroom, Timetable, SubjectAssignment, FeeStructure, Payment, Parent

# ---- STUDENT ----
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

# ---- COURSE ----
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

# ---- GRADE ----
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"

# ---- ATTENDANCE ----
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

# ---- TEACHER ----
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

# ---- CLASSROOM ----
class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"

# ---- TIMETABLE ----
class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = "__all__"

# ---- SUBJECT ASSIGNMENT ----
class SubjectAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectAssignment
        fields = "__all__"

# ---- FEES ----
class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = "__all__"

# ---- PAYMENTS ----
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

# ---- PARENT ----
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"
