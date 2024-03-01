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

