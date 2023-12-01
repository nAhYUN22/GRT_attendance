from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, View
from rest_framework import generics
from django.contrib.auth import login
import json

from .models import Student, MeetingTime

from .serializers import LoginUserSerializer, UserSeriazlizer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        serializer = self.get_serializer(data=data)
        # if not serializer.is_valid():
        #     print(serializer.errors)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        print(user.ID)
        print(user)
        login(request, user)
        print("login\n")
        return Response({
                         'ID':user.ID,
                         'token':token.key
                         })
        
class CheckLoginView(generics.GenericAPIView):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            print("login")
            # 사용자가 로그인한 경우
            return JsonResponse({'logged_in': True})
        else:
            print("no login")
            # 사용자가 로그인하지 않은 경우
            return JsonResponse({'logged_in': False})

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

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    
class LoginPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')