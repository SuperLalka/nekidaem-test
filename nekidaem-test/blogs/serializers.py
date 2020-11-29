from rest_framework import serializers

from . import models


class BlogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Blog
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        exclude = ['created_at']
