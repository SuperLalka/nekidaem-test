from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from rest_framework import permissions as drf_permissions

from . import models, permissions, serializers


def user_blog(request):
    extendinguser = models.ExtendingUser.objects.get(user=request.user)
    blog = models.Blog.objects.get(user=extendinguser)
    posts_list = models.Post.objects.filter(blog=blog)
    return render(request, 'blog_page.html', context={
        'blog': blog,
        'posts_list': posts_list,
    })


class UserBlogDetailView(generic.DetailView):
    model = models.Blog
    pk_url_kwarg = 'blog_id'
    template_name = 'blog_page.html'

    def get_context_data(self, **kwargs):
        post_list = models.Post.objects.filter(blog=self.object)
        context = {
            'posts_list': post_list,
            **kwargs
        }
        return super().get_context_data(**context)


class NewsFeedDetailView(generic.DetailView):
    model = models.Blog
    pk_url_kwarg = 'blog_id'
    template_name = 'news_feed_page.html'

    def get_context_data(self, **kwargs):
        list_of_subscriptions = self.object.user.subscribed_to.all()
        news_list = models.Post.objects.filter(
            blog__id__in=[obj.id for obj in list_of_subscriptions]).exclude(
            read_by_user=self.request.user.extendinguser
        )
        context = {
            'list_of_subscriptions': list_of_subscriptions,
            'news_list': news_list,
            **kwargs
        }
        return super().get_context_data(**context)


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
