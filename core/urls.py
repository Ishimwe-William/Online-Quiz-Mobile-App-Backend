"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )

from users.views import LogoutViewSet

urlpatterns = [
    path('admin/', admin.site.urls),

    # http://localhost:8000/auth/login/google-oauth2/
    path('auth/', include('social_django.urls', namespace='social')),
    # path('auth/logout/', LogoutViewSet.as_view, name="auth-logout"),
    path('api/users/', include('users.urls', namespace='users')),  # url endpoint for users
    path('api/', include('quiz_api.urls', namespace='quiz_api')),  # url endpoint for main api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
