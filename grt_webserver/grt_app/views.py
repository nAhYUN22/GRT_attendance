from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, View
from rest_framework import generics
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
import json
import requests
import os

from .models import Student, MeetingTime
from .forms import StudentForm, StudentSearchForm, MeetingTimeForm
from .serializers import LoginUserSerializer, UserSeriazlizer

from django.views.generic.list import ListView

class LoginView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    
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

def logout(request):
    auth_logout(request)
    return render(request, 'index.html')

class StudentListView(View):
    def get(self, request, *args, **kwargs):
        form = StudentSearchForm(request.GET or None)
        if form.is_valid() and form.cleaned_data['name']:
            students = Student.objects.filter(name__icontains=form.cleaned_data['name'])
            for student in students:
                print(student.id)
        else:
            students = Student.objects.all()
            for student in students:
                print(student)
        return render(request, 'studentlist.html', {'form': form, 'students': students})

class MeetingListView(View):
    def get(self,request, *args, **kwargs):
        student_zoom_id = request.GET.get('student_zoom_id')
        student = Student.objects.get(zoom_id=student_zoom_id)
        try:
            meetings = MeetingTime.objects.filter(zoom_id=student_zoom_id)
        except:
            meetings = None
        data={
            'student':student,
            'meetings':meetings
        }
        return render(request,'meetinglist.html',data)


class AddStudentView(View):    
    def get(self, request, *args, **kwargs):
        form = StudentForm()
        return render(request, 'addstudent.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            student=form.save(commit=False)
            print(student.id)
            student.save()
            print(student)
            return redirect('addstudent')

    
class AddMeetingView(View):
    def get(self, request, *args, **kwargs):
        student_zoom_id = request.GET.get('student_zoom_id')
        student = Student.objects.get(zoom_id=student_zoom_id)
        print(student.zoom_id)
        form = MeetingTimeForm(initial={'zoom_id':student_zoom_id})
        return render(request,'addmeeting.html',{'form':form,
                                                 'student':student})
    
    def post(self, request, *args, **kwargs):
        form = MeetingTimeForm(request.POST)
        if form.is_valid():
            meeting_time = form.save()
            # print(meeting_time)
            # student_zoom_id = request.POST.get('student_zoom_id')
            # meeting_time.zoom_id = student_zoom_id  # MeetingTime 객체에 student 할당
            # meeting_time.save()
            print("success")
            return redirect('studentlist')
        else:
            print(form.errors)
            return render(request, 'studentlist.html', {'success':"No"})
        
class CreateMeetingView(View):
    def get(self,request,*args, **kwargs):
        # replace with your client ID
        client_id = os.environ.get('CLIENT_ID')

        # replace with your account ID
        account_id = os.environ.get('ACCOUNT_ID')

        # replace with your client secret
        client_secret = os.environ.get('CLIENT_SECRET')
        print(client_id)
        print(account_id)
        print(client_id)

        auth_token_url = "https://zoom.us/oauth/token"
        api_base_url = "https://api.zoom.us/v2"
        data={
            "grant_type": "account_credentials",
            "account_id": account_id,
            "client_secret": client_secret
        }
        response = requests.post(auth_token_url,auth=(client_id,client_secret),data=data)

        if response.status_code!=200:
                print("Unable to get access token")
        else:
            print("Success")
        response_data = response.json()
        access_token = response_data["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        start_date="2023-12-28"
        start_time="17:43"
        payload = {
            "topic": "test",
            "duration": "60",
            'start_time': f'{start_date}T10:{start_time}',
            "type": 2
        }

        resp = requests.post(f"{api_base_url}/users/me/meetings", 
                             headers=headers, 
                             json=payload)

        if resp.status_code!=201:
            print("Unable to generate meeting link")
        response_data = resp.json()

        content = {
                        "meeting_url": response_data["join_url"], 
                        "password": response_data["password"],
                        "meetingTime": response_data["start_time"],
                        "purpose": response_data["topic"],
                        "duration": response_data["duration"],
                        "message": "Success",
                        "status":1
        }
        print(content)
        return render(request,'index.html',{'status':"success"})
        
class CheckParticiapantsView(View):
    def post():
        return

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')