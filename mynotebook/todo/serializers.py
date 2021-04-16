from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import ListField, ChoiceField, BooleanField
from rest_framework.serializers import Serializer

from .models import Note


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class SmallAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class PublicNotesSerializer(serializers.ModelSerializer):
    author = SmallAuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'author')


class PublicNoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"


class MyNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'status', 'important', 'public', 'date_to_complete')


class MyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ['author']


class MyNoteEditSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['date_edited', 'author', ]


class QuerySerializer(Serializer):
    status = ListField(child=ChoiceField(choices=Note.STATUS_CHOICES), required=False)
    important = BooleanField(required=False)
    public = BooleanField(required=False)
