from django.contrib import admin

from .models import Post, Category, Comment, Profile

def active_comment(modeladmin, request, queryset):
    queryset.update(active=True)

active_comment.short_description = 'Mark As Active Comment'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'active']
    actions = [active_comment]

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)