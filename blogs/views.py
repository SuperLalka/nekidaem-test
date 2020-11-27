from rest_framework import viewsets
from rest_framework import permissions as drf_permissions

from . import models, permissions, serializers


class BlogsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    permission_classes = [drf_permissions.IsAuthenticated]
    serializer_class = serializers.BlogsSerializer
    queryset = models.Blog.objects.all()


class PostsViewSet(viewsets.ModelViewSet):
    filterset_fields = ['blog']
    lookup_field = 'id'
    permission_classes = [drf_permissions.IsAuthenticated]
    serializer_class = serializers.PostsSerializer
    queryset = models.Post.objects.all()

    permission_classes_by_action = {
        'create': [permissions.MasterPermissions],
        'retrieve': [],
        'list': [],
        'update': [permissions.MasterPermissions],
        'partial_update': [permissions.MasterPermissions],
        'destroy': [permissions.MasterPermissions]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
