from django import forms
from .models import Student, Course, Attendance, Grade, Teacher, Classroom, Timetable, SubjectAssignment, FeeStructure, Payment, SchoolSetting

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'department', 'classroom']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department']
        labels = {
            'name': 'Title',  # <-- this is the key change
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'score']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['full_name', 'staff_id', 'email', 'phone', 'department', 'qualification', 'date_joined']

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'description', 'teacher']      

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['day', 'period', 'classroom', 'subject', 'teacher']      


class SubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubjectAssignment
        fields = ['classroom', 'subject', 'teacher']


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['classroom', 'term', 'session', 'amount']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'term', 'session', 'amount_paid', 'reference']

class FeeForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class SchoolSettingForm(forms.ModelForm):
    class Meta:
        model = SchoolSetting
        fields = [
            'school_name', 
            'slogan', 
            'current_session', 
            'current_term', 
            'dashboard_bg', 
            'contact_email', 
            'contact_phone'
        ]
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'slogan': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'current_session': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'current_term': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'dashboard_bg': forms.FileInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'contact_email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
            'contact_phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-xl'}),
        }

#class ParentForm(forms.ModelForm):
 #   class Meta:
  #      model = Parent
   #     fields = '__all__'   # includes user, full_name, phone, student