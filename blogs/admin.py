from django.contrib import admin

from . import models


@admin.register(models.ExtendingUser)
class ExtendingUserAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'header', 'created_at')
    search_fields = ('blog', 'header')
    date_hierarchy = 'created_at'
