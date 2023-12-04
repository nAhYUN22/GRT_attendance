from django import forms
from .models import Student, MeetingTime

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'zoom_id', 'phone_num']

class MeetingTimeForm(forms.ModelForm):
    class Meta:
        model = MeetingTime
        fields = ['date', 'start_time']