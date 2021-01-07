from django.contrib import admin

from blogs.models import (
    Blog, Post, User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'header', 'created_at')
    search_fields = ('blog', 'header')
    date_hierarchy = 'created_at'
