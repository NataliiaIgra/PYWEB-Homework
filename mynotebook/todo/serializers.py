from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers


from .models import Note


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class NoteListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'text', 'public', 'author']  # ???


class NoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        exclude = ('public', )
