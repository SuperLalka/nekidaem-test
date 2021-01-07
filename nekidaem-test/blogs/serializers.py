from rest_framework import serializers

from .models import (
    Blog, Post
)


class BlogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ['created_at']
