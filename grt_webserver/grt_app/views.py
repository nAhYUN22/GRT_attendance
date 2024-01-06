from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponseRedirect
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
from .forms import StudentForm, StudentSearchForm, MeetingTimeForm, MeetingRoomForm
from .serializers import LoginUserSerializer, UserSeriazlizer
from .services import WebexServices, AttendanceServices

class LoginView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.get_serializer(data=data)
        # if not serializer.is_valid():
        #     print(serializer.errors)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        # print("login\n")
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

class LogoutView(View):
    def get(self, request, *args, **kwargs):
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
        student_email = request.GET.get('student_email')
        print(student_email)
        student = Student.objects.get(email=student_email)
        try:
            meetings = MeetingTime.objects.filter(email=student_email)
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
        student_email = request.GET.get('student_email')
        student = Student.objects.get(email=student_email)
        # print(student.email)
        form = MeetingTimeForm(initial={'email':student_email})
        return render(request,'addmeeting.html',{'form':form,
                                                 'student':student})
    
    def post(self, request, *args, **kwargs):
        form = MeetingTimeForm(request.POST)
        if form.is_valid():
            meeting_time = form.save()
            # print(meeting_time)
            # student_email = request.POST.get('student_email')
            # meeting_time.zoom_id = student_email  # MeetingTime 객체에 student 할당
            # meeting_time.save()
            print("success")
            return redirect('studentlist')
        else:
            print(form.errors)
            return render(request, 'studentlist.html', {'success':"No"})
        
# class CreateMeetingView(View):
#     def get(self,request,*args, **kwargs):
#         meeting=ZoomServices()
#         meeting.create_meeting()
#         return render(request,'index.html',{'status':"success"})
        
class CheckAttendanceView(View):
    def get(self, request, *args, **kwargs):
        form = MeetingRoomForm(request.GET)
        if form.is_valid() and form.cleaned_data['room']:
            meetingnum=form.cleaned_data['room']
            # meeting=ZoomServices()
            meeting=WebexServices()
            meetingId=meeting.get_meeting_id(meetingnum)
            participants=meeting.get_participants(meetingId)
            # response=meeting.get_participants(meetingId)
            # participants=response.get("participants",[])
            print(participants)
            time=AttendanceServices()
            registrants=time.get_registrants()
            print(registrants)
            # meeting.check_attendance(participants=participants)
            absent=[p for p in registrants if p not in participants]
            print(absent)
            
            # 부재중인 참가자들의 이름 가져오기
            absent_students = list(Student.objects.filter(email__in=absent))
            # .values_list('name', flat=True)
            # absent_names = list(absent_students)
            # print(absent_names)
            return render(request, 'checkattendance.html',{'form': form,
                                                       'absents':absent_students})
        return render(request, 'checkattendance.html',{'form': form})
        
        
class GetParticipantView(View):
    def post(self,request,*args, **kwargs):
        response=json.loads(request.body)
        participant=response['participant']
        print(participant)
        
class RequestPermissionView(View):
    def get(self,request,*args, **kwargs):
        oauth_url=WebexServices().get_oauth_url()
        return redirect(oauth_url)
        # return HttpResponseRedirect(oauth_url)

class OauthView(View):
    def get(self,request, *args,**kwargs):
        state=request.GET.get('state')
        code=request.GET.get('code')
        
class TestView(View):
    def get(self, request, *args, **kwargs):
        time=AttendanceServices()
        time_now=time.get_registrants()
        print(time_now)
        return JsonResponse({"time": time_now})

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')