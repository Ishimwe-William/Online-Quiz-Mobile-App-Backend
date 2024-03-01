from django.urls import path

from users.views import UserList, UserDetail, Register

app_name = 'users'

urlpatterns = [
    path('', UserList.as_view(), name='listUsers'),
    path('register/', Register.as_view(), name='register'),
    path('<int:pk>/', UserDetail.as_view(), name='userDetails'),
]
