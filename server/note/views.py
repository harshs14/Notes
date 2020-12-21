from rest_framework.views import APIView
from .models import Notes
from rest_framework import permissions, viewsets
from .serializers import NotesSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class NotesView(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Notes.objects.all()

    @action(methods=['GET'], detail=False)
    def bookmarks(self, request, *args, **kwargs):
        bookmarkedNotes = Notes.objects.filter(bookmark=True)
        serializer = NotesSerializer(bookmarkedNotes, many=True)
        return Response(serializer.data)
