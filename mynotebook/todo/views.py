from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Note
from .serializers import NoteListSerializer, NoteSerializer


def about(request):
    ...


class NoteListView(APIView):
    def get(self, request):
        notes = Note.objects.filter(public=True).order_by('date_edited', 'title') # [0:3]  # pagination???
        notes_serializer = NoteListSerializer(notes, many=True)
        return Response(notes_serializer.data)


class NoteView(APIView):
    def get(self, request, note_id):
        note = Note.objects.filter(pk=note_id, public=True).first()

        if not note:
            raise NotFound(f'Note with id = {note_id} was not found')

        note_serializer = NoteSerializer(note)
        return Response(note_serializer.data)


class NoteEditView(APIView):
    permission_classes = (IsAuthenticated, )



class NoteListViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteListSerializer
    permission_classes = [permissions.IsAuthenticated]
