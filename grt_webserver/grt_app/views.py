from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import login
import json

from .serializers import LoginUserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({"message": "User logged in successfully."})


# Create your views here.
def user_login(request):
    username=request.POST.get('username')
    password=request.POSt.get('password')
    user=authenticate(request, username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('home')
    else:
        return render(request, 'login.html',{'error': 'Invalid ID or PW'})
    return render(request,'login.html')


def index(request):
    return render(request,'index.html')