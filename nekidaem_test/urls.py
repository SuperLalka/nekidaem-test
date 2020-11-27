from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views


tokens_url = [
    path('', jwt_views.TokenObtainPairView.as_view()),
    path('refresh/', jwt_views.TokenRefreshView.as_view()),
    path('verify/', jwt_views.TokenVerifyView.as_view()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', include(tokens_url)),
    path('', include('blogs.urls')),
]
