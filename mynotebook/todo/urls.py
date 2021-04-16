from django.urls import path

from .views import AboutView, PublicNotesView, PublicNoteView, MyNotesView, MyNoteView

urlpatterns = [
    path('about/', AboutView.as_view()),
    path('notes/', PublicNotesView.as_view()),
    path('notes/<int:note_id>', PublicNoteView.as_view()),
    path('mynotes/', MyNotesView.as_view()),
    path('mynotes/<int:note_id>', MyNoteView.as_view()),
]
