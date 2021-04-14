from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_to_complete', 'author', 'status', 'important', 'public', 'date_edited')
    search_fields = ['title', 'text']
    list_filter = ('public', 'important', 'status')
    ordering = ('-date_edited', 'important')
    list_display_links = ('title',)
    readonly_fields = ('author', )

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
