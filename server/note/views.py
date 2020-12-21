from rest_framework.views import APIView
from .models import Notes
from rest_framework import permissions, status, viewsets
from .serializers import NotesSerializer
from rest_framework.response import Response

class NotesView(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Notes.objects.all()


