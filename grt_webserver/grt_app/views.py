from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, View
from rest_framework import generics
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
import json

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

# ListView 활용
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

# # ListView 활용 X
# class StudentListView(View):
#     def get(self, request, *args, **kwargs):
#         students = Student.objects.all()  # 모든 학생 데이터를 가져옵니다.
#         return render(request, 'student_list.html', {'students': students})


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
    

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')