from django.conf.urls import url
from django.urls import include
from django.views.generic import RedirectView

from rest_framework.routers import DefaultRouter
from . import views


routerAPI = DefaultRouter()
routerAPI.register(r'blogs', views.BlogsViewSet, basename='blogs')
routerAPI.register(r'posts', views.PostsViewSet, basename='posts')


app_name = 'blogs'
urlpatterns = [
    url(r'^api/', include(routerAPI.urls)),
    url(r'^blog/(?P<blog_id>\d+)', views.UserBlogDetailView.as_view(), name='blog'),
    url(r'^news_feed/(?P<blog_id>\d+)', views.NewsFeedDetailView.as_view(), name='news_feed'),
    url(r'^user_blog/', views.user_blog, name='user_blog'),
    url(r'^$', RedirectView.as_view(url='user_blog/', permanent=True)),
]
