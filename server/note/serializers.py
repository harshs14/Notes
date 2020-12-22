from rest_framework import serializers
from .models import Notes, Otp
from django.contrib.auth import get_user_model
import re
from rest_framework.exceptions import ValidationError

User = get_user_model()

class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ('createdOn', 'modifiedOn', 'user',)

class OtpSerialaizer(serializers.ModelSerializer):
    
    class Meta:
        model = Otp
        fields = ('userId', 'otp',)
        read_only_fields = ('userId',)

class UserSignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
    )
    # last_name = serializers.CharField(
    #     required=True,
    # )
    email = serializers.EmailField(
        required=True, 
    )
    password = serializers.CharField(
        required=True, 
        style={'input_type': 'password'},
    )
    confirmPassword = serializers.CharField(
        required=True, 
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirmPassword')

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')

        try:
            user = User.objects.filter(email=email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user:
            raise ValidationError({'error': 'Email already exists'})
             
        if len(username) < 5:
            raise ValidationError({'error': 'Username must have minimum 5 characters'})

        if password != confirmPassword :
            raise ValidationError({'error': 'Passwords mismatch'})
        
        try:
            user = User.objects.get(username = username)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user:
            raise ValidationError({'error': 'Username already exists'})

        return data



class UserLoginSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        required=True, 
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = ('username', 'password',)

# class UserProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'username',)
#         read_only_fields = ('email', 'username',)
