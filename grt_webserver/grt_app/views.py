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
from .forms import StudentForm
from .serializers import LoginUserSerializer, UserSeriazlizer

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

class AddStudentView(View):
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addstudent')
    
    def get(self, request, *args, **kwargs):
        form = StudentForm()
        return render(request, 'addstudent.html', {'form': form})

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')