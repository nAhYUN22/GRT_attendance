from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import login
import json

from .models import Student, MeetingTime

from .serializers import LoginUserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({"message": "User logged in successfully."})

class AddStudentMeetingView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        
        student_data = data.get('student')
        student, created=Student.objects.get_or_create(
            name=student_data['name'],
            zoom_id=student_data['zoom_id']
        )
        
        meeting_time_data = data.get('meeting_times')
        for mt_data in meeting_time_data:
            MeetingTime.objects.create(
                student=student,
                date=mt_data['date'],
                start_time=mt_data['start_time'],
                end_time=mt_data['end_time']
            )
        
        return JsonResponse({'status':'success'})

# Create your views here.
def user_login(request):
    user_id=request.POST.get('id')
    password=request.POSt.get('password')
    user=authenticate(request, username=user_id,password=password)
    if user is not None:
        login(request,user)
        return redirect('home')
    else:
        return render(request, 'login.html',{'error': 'Invalid ID or PW'})
    return render(request,'login.html')


def index(request):
    return render(request,'index.html')


        
    
    