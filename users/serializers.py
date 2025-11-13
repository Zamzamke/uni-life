from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="User password (min 8 characters)"
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm password"
    )
    
    class Meta:
        model = User
        fields = ('email', 'full_name', 'role', 'password', 'password2')
        extra_kwargs = {
            'email': {'help_text': 'User email address (must be unique)'},
            'full_name': {'help_text': 'User full name'},
            'role': {'help_text': 'User role (student or admin)'},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'date_joined', 'last_login')
        read_only_fields = ('id', 'date_joined', 'last_login')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
        extra_kwargs = {
            'university': {'help_text': 'University or institution name'},
            'course': {'help_text': 'Course or program of study'},
            'year': {'help_text': 'Year of study'},
            'bio': {'help_text': 'Personal biography or description'},
            'avatar_url': {'help_text': 'URL to profile picture'},
        }

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('university', 'course', 'year', 'bio', 'avatar_url')