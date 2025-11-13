from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Profile
from .serializers import UserRegistrationSerializer, UserSerializer, ProfileSerializer, ProfileUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Schema definitions for Swagger
register_schema = swagger_auto_schema(
    method='post',
    request_body=UserRegistrationSerializer,
    responses={
        201: openapi.Response('User created successfully', UserRegistrationSerializer),
        400: 'Bad Request - Validation error'
    }
)

login_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
        }
    ),
    responses={
        200: openapi.Response('Login successful', examples={
            'application/json': {
                'user': {
                    'id': 'uuid',
                    'email': 'user@example.com',
                    'full_name': 'John Doe',
                    'role': 'student'
                },
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
            }
        }),
        401: 'Invalid credentials'
    }
)

@register_schema
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_schema
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(email=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    
    return Response(
        {'error': 'Invalid credentials'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )

@swagger_auto_schema(method='get', responses={200: ProfileSerializer})
@swagger_auto_schema(method='put', request_body=ProfileUpdateSerializer, responses={200: ProfileSerializer})
@api_view(['GET', 'PUT'])
def profile_view(request):
    if request.method == 'GET':
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)