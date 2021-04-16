from django.views import View
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mynotebook import settings
from .models import Note
from .serializers import *


class AboutView(View):
    def get(self, request):
        context = {'server_version': settings.SERVER_VERSION,
                   'message': 'Welcome :)'}
        return render(request, 'about.html', context)


class PublicNotesView(APIView, LimitOffsetPagination):
    def get(self, request):
        notes = Note.objects.filter(public=True).order_by('date_to_complete', '-important')
        notes = self.paginate_queryset(notes, request, view=self)
        notes_serializer = PublicNotesSerializer(notes, many=True)
        return self.get_paginated_response(notes_serializer.data)


class PublicNoteView(APIView):
    def get(self, request, note_id):
        note = Note.objects.filter(pk=note_id, public=True).first()

        if not note:
            raise NotFound(f'Note with id = {note_id} was not found')

        note_serializer = PublicNoteSerializer(note)
        return Response(note_serializer.data)


class MyNotesView(APIView, LimitOffsetPagination):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        notes = Note.objects.filter(author=request.user).order_by('date_to_complete', '-important')
        query_params = QuerySerializer(data=request.query_params)

        if query_params.is_valid():
            if 'important' in request.query_params:
                notes = notes.filter(important=query_params.data['important'])

            if 'public' in request.query_params:
                notes = notes.filter(important=query_params.data['public'])

            if query_params.data.get('status'):
                q_status = Q()
                for i in query_params.data['status']:
                    q_status |= Q(status=i)
                notes = notes.filter(q_status)

        else:
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)

        notes = self.paginate_queryset(notes, request, view=self)
        notes_serializer = MyNotesSerializer(notes, many=True)
        return self.get_paginated_response(notes_serializer.data)

    def post(self, request):
        new_note = MyNoteEditSerializer(data=request.data)
        if new_note.is_valid():
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)


class MyNoteView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, note_id):
        note = Note.objects.filter(pk=note_id, author=request.user).first()

        if not note:
            raise NotFound(f'Note with id = {note_id} for user {request.user.username} was not found')

        note_serializer = MyNoteSerializer(note)
        return Response(note_serializer.data)

    def patch(self, request, note_id):
        note = Note.objects.filter(pk=note_id, author=request.user).first()

        if not note:
            raise NotFound(f'Note with id = {note_id} for user {request.user.username} was not found')

        new_note = MyNoteEditSerializer(note, data=request.data, partial=True)

        if new_note.is_valid():
            new_note.save()
            return Response(new_note.data, status=status.HTTP_200_OK)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = Note.objects.filter(pk=note_id, author=request.user).first()

        if not note:
            raise NotFound(f'Note with id = {note_id} for user {request.user.username} was not found')

        note.delete()
        return Response(f'Note with id = {note_id} was deleted', status=status.HTTP_200_OK)
