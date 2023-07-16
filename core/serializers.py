from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class PasswordField(serializers.CharField):
    def __init__(self, validate: bool = True, **kwargs) -> None:
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)
        if validate:
            self.validators.append(validate_password)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = PasswordField()
    password_repeat = PasswordField(validate=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']
        # extra_kwargs = {
        #     'password': {'write_only': True},
        # }

    def validate(self, data):
        password = data.get('password')
        password_repeat = data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data['password']
        )
        return User.objects.create(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError("Wrong password.")
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        if user.check_password(value):
            raise serializers.ValidationError("New password must be different from the old password.")
        return value

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.password = make_password(new_password)
        instance.save()
        return instance