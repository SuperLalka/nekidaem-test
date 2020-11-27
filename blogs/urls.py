from django.conf.urls import url
from django.urls import include

from rest_framework.routers import DefaultRouter
from . import views


routerAPI = DefaultRouter()
routerAPI.register(r'blogs', views.BlogsViewSet, basename='blogs')
routerAPI.register(r'posts', views.PostsViewSet, basename='posts')


app_name = 'custom_requests'
urlpatterns = [
    url(r'^api/', include(routerAPI.urls)),
]
