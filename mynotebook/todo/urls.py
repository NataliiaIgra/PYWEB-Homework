from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import NoteListView, NoteView, NoteEditView, AboutView

urlpatterns = [
    path('note/', NoteListView.as_view()),
    # path('note/<int:note_id>', NoteView.as_view()),
    # path('note/add/', NoteEditView.as_view()),
    # path('', include(router.urls)),
    path('about/', AboutView.as_view()),
]
