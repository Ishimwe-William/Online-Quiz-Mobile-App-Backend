from rest_framework import generics
# from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated\
    # , IsAdminUser
from users.models import User
from users.serializers import CustomUserSerializer \
    # , ResetCustomUserPasswordSerializer, MakeCustomUserInactiveActiveSerializer


# Create a user
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer


# Get all users
class UserList(generics.ListAPIView):
    # queryset = User.non_superuser_objects.all()  # only non-superuser
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    # Only authenticated user can access users list
    permission_classes = [AllowAny]


# Get single user | update a single user
class UserDetail(generics.RetrieveUpdateAPIView):
    # queryset = User.non_superuser_objects.all()  # only non-superuser
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

# # Get single user | reset user password
# class ResetCustomUserPassword(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = ResetCustomUserPasswordSerializer
#     permission_classes = [AllowAny]

#
# # Get single user | make user inactive
# class ManageUserStatus(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = MakeCustomUserInactiveActiveSerializer
#     # Only admin can make user inactive/active
#     permission_classes = [IsAdminUser]
