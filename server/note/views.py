import random
from threading import Thread
from rest_framework.views import APIView
from .models import Notes, Otp
from rest_framework import permissions, viewsets
from .serializers import NotesSerializer, OtpSerialaizer, UserSignupSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from server.settings import EMAIL_HOST_USER

def sendMail(user):
    
    try:
        otp = Otp.objects.filter(userId = user)
    except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
        otp = None
    if otp is not None:
        otp.delete()

    otp = random.randint(1000,10000)
    otpObj = Otp.objects.create(userId = user, otp = otp)

    subject = 'NOTES VERIFICATION'
    message = 'YOUR OTP : ' + str(otpObj.otp)
    to_mail = [user.email]
    from_mail = EMAIL_HOST_USER
    send_mail(subject, message, from_mail, to_mail, fail_silently=False)

class NotesView(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Notes.objects.all()

    def perform_update(self, serializer):
        serializer.save(modifiedOn = timezone.now())

    @action(methods=['GET'], detail=False)
    def bookmarks(self, request, *args, **kwargs):
        bookmarkedNotes = Notes.objects.filter(bookmark=True)
        serializer = NotesSerializer(bookmarkedNotes, many=True)
        return Response(serializer.data)

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

            user = User.objects.create(
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