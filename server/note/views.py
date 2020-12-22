from rest_framework.views import APIView
from .models import Notes
from rest_framework import permissions, viewsets
from .serializers import NotesSerializer, OtpSerialaizer, UserSignupSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

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

            return Response({'info': 'Signup Successful', 'userId': user.id})
        raise ValidationError({'error': 'Invalid User'})