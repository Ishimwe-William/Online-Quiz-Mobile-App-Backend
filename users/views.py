import logging

import firebase_admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import generics, viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from firebase_admin import auth


from users.models import User
from users.serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from firebase_admin import credentials

# Initialize the Firebase SDK
cred = credentials.Certificate('core/online-quiz-mobile-app-firebase-adminsdk-avvbd-839f9174e8.json')
firebase_admin.initialize_app(cred)

logger = logging.getLogger(__name__)


class FirebaseTokenVerificationView(APIView):
    def post(self, request):
        # Extract Firebase ID token from the request
        id_token = request.data.get('idToken', None)

        if not id_token:
            logger.error('No ID token provided')
            return Response({'error': 'No ID token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            # Extract user email from decoded token
            user_email = decoded_token.get('email')

            # Check if email is present
            if not user_email:
                logger.error('Email not found in token')
                return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)

            # Search for user in database by email
            try:
                user = User.objects.get(email=user_email)
            except ObjectDoesNotExist:
                logger.error('User not found for email: %s', user_email)
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Serialize user data
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except auth.ExpiredIdTokenError:
            logger.error('Expired ID token')
            return Response({'error': 'Expired ID token'}, status=status.HTTP_400_BAD_REQUEST)
        except auth.InvalidIdTokenError:
            logger.error('Invalid ID token')
            return Response({'error': 'Invalid ID token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception('Exception occurred: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create a user
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                # Handle unique constraint violation error
                if 'email' in str(e):
                    message = {'email': ['This email address is already in use.']}
                elif 'username' in str(e):
                    message = {'username': ['This username is already taken.']}
                else:
                    message = {'detail': 'Unique constraint violated.'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Re-raise the exception if it's not a unique constraint violation error
                raise


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
