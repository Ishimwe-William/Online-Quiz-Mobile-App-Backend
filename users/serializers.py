# from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers

from users.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    # Some validations
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'firstname', 'lastname', 'username',
            'password', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # hashing password
            instance.set_password(password)
        instance.save()
        return instance


# class ResetCustomUserPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(min_length=8, write_only=True)
#
#     def update(self, instance, validated_data):
#         password = validated_data.get('password')
#         if password and not check_password(password, instance.password):
#             # Only update the password if it's different from the existing one
#             instance.password = make_password(password)
#             instance.save()
#         return instance
#
#
# class MakeCustomUserInactiveActiveSerializer(serializers.Serializer):
#     is_active = serializers.BooleanField()
#
#     def update(self, instance, validated_data):
#         is_active = validated_data.get('is_active')
#         if is_active is not None:
#             instance.is_active = is_active
#         instance.save()
#         return instance
