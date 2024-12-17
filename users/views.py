from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserInputOutput
from .serializers import UserInputOutputSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'User registered successfully'}, status=201)

def home_view(request):
    return JsonResponse({"message": "Welcome to SpecWise API!"})

class CheckUsernameView(APIView):
    def get(self, request, username):
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            return JsonResponse({'message': 'Login successful', 'username': username}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)


class UserInputOutputView(generics.CreateAPIView):
    queryset = UserInputOutput.objects.all()
    serializer_class = UserInputOutputSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Save the logged-in user
