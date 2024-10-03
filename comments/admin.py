from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username')