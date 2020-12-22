import random
from threading import Thread
from rest_framework.views import APIView
from .models import Notes, Otp
from rest_framework import permissions, viewsets
from .serializers import NotesSerializer, OtpSerialaizer, UserSignupSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from server.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from .permissions import IsOwner

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh.payload['sub'] = user.id
    refresh.payload['iat'] = datetime.now()
    refresh.access_token.payload['sub'] = user.id
    refresh.access_token.payload['iat'] = datetime.now()
    return str(refresh), str(refresh.access_token)

def sendMail(user):
    try:
        otp = Otp.objects.filter(user = user)
    except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
        otp = None
    if otp is not None:
        otp.delete()

    otp = random.randint(1000,10000)
    otpObj = Otp.objects.create(user = user, otp = otp)

    subject = 'NOTES VERIFICATION'
    message = 'YOUR OTP : ' + str(otpObj.otp)
    to_mail = [user.email]
    from_mail = EMAIL_HOST_USER
    print(from_mail)
    send_mail(subject, message, from_mail, to_mail, fail_silently=False)

class UserSignupView(APIView):
    serializer_class = UserSignupSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                username=username, 
                password=password
            )

            user.is_active = False
            user.save()

            emailThread = Thread(target = sendMail, args=(user,))
            emailThread.start()

            return Response({'info': 'Signup Successful', 'userId': user.id})
        raise ValidationError({'error': 'Invalid User'})

class UserVerificationView(APIView):
    serializer_class = OtpSerialaizer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, userId, *args, **kwargs):
        serializer = OtpSerialaizer(data = request.data)
        code = request.data['otp']
        try:
            otp = Otp.objects.get(user = userId)
        except(TypeError, ValueError, OverflowError, Otp.DoesNotExist):
            otp = None
        
        try:
            user = User.objects.get(id = userId)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if not otp or not user:
            return Response({'error': 'Invalid user'})

        elif timezone.now() - otp.timestamp >= timedelta(minutes=1):
            return Response({'error': 'OTP expired'})

        elif str(otp.otp) == str(code):
            user.is_active = True
            user.save()
            otp.delete()
            refresh, access = get_tokens_for_user(user)
            
            return Response({'info': 'User verified', 'refresh': refresh, 'access': access}) 
        return Response({'error':'Invalid Otp'})

class ResendOtpView(APIView):
    serializer_class = OtpSerialaizer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, userId, *args, **kwargs):
        try:
            user = User.objects.get(id = userId)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            emailThread = Thread(target = sendMail, args=(user,))
            emailThread.start()

            return Response({'info': 'Otp Sent'})
        raise ValidationError({'error': 'Invalid user'})

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                refresh, access = get_tokens_for_user(user)
                login(request, user)
                return Response({'info': 'Successful login', 'refresh': refresh, 'access': access})
            return Response({'error': 'User not verified'})
        return Response({'error': 'Inavalid Credentials'})

class UserLogoutView(APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'info': 'logged out'})

class NotesView(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Notes.objects.all()

    def list(self, request):
        queryset = Notes.objects.filter(user = request.user.id)
        serializer = NotesSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
            serializer.save(user = self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(modifiedOn = timezone.now())

    @action(methods=['GET'], detail=False)
    def bookmarks(self, request, *args, **kwargs):
        bookmarkedNotes = Notes.objects.filter(bookmark=True, user=self.request.user)
        serializer = NotesSerializer(bookmarkedNotes, many=True)
        return Response(serializer.data)