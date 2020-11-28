from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets, mixins
from rest_framework import permissions as drf_permissions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

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
        read_posts = self.object.user.read_posts.all()
        news_list = models.Post.objects.filter(
            blog__id__in=[obj.id for obj in list_of_subscriptions]).exclude(
            id__in=[obj.id for obj in read_posts])
        context = {
            'list_of_subscriptions': list_of_subscriptions,
            'news_list': news_list,
            **kwargs
        }
        return super().get_context_data(**context)


class PostsViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    permission_classes = [drf_permissions.IsAuthenticated]
    serializer_class = serializers.PostsSerializer
    queryset = models.Post.objects.all()

    permission_classes_by_action = {
        'create': [permissions.MasterPermissions],
        'update': [permissions.MasterPermissions],
        'partial_update': [permissions.MasterPermissions],
        'destroy': [permissions.MasterPermissions]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @action(methods=('post', ), detail=True)
    def mark_readed(self, request, pk):
        post = models.Post.objects.get(id=pk)
        if post.blog in request.user.extendinguser.subscribed_to.all():
            self.request.user.extendinguser.read_posts.add(post)
            return HttpResponse('Post ' + post.header + ' added to read')
        return HttpResponse('User is not subscribed to this blog')


class BlogsViewSet(GenericViewSet):
    lookup_field = 'blog_id'
    permission_classes = [drf_permissions.IsAuthenticated]

    @action(methods=('post', ), detail=True)
    def subscribe(self, request, blog_id):
        blog = models.Blog.objects.get(id=blog_id)
        self.request.user.extendinguser.subscribed_to.add(blog)
        return HttpResponse('You subscribed to the blog ' + blog.user.__str__())

    @action(methods=('post',), detail=True)
    def unsubscribe(self, request, blog_id):
        blog = models.Blog.objects.get(id=blog_id)
        self.request.user.extendinguser.subscribed_to.remove(blog)
        marked_posts = models.Post.objects.filter(blog=blog)
        [self.request.user.extendinguser.read_posts.remove(obj.id) for obj in marked_posts]
        return HttpResponse('You have unsubscribed from the blog ' + blog.user.__str__())
