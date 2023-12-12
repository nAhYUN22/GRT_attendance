from django import forms
from .models import Student, MeetingTime

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'zoom_id', 'phone_num']

# class MeetingTimeForm(forms.ModelForm):
#     class Meta:
#         model = MeetingTime
#         fields = ['date', 'start_time']
        
class StudentSearchForm(forms.Form):
    name = forms.CharField(required=False, label='학생 이름')
    
class MeetingTimeForm(forms.ModelForm):
    class Meta:
        model = MeetingTime
        fields = ['zoom_id', 'date', 'start_time']  # 필요한 필드를 여기에 추가합니다.