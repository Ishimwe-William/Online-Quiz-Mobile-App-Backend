from rest_framework import generics, viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


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


class LogoutViewSet(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        refresh = request.data.get("refresh")
        if refresh is None:
            raise ValidationError({
                "detail": "A refresh token is required."
            })
        try:
            token = RefreshToken(request.data.get("refresh"))
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError:
            raise ValidationError({"detail": "The refresh token is invalid."})
