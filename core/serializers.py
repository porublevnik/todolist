from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class PasswordField(serializers.CharField):
    '''
    Сериализатор для поля "пароль" модели User
    '''
    def __init__(self, validate: bool = True, **kwargs) -> None:
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)
        if validate:
            self.validators.append(validate_password)


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для регистрации пользователя
    '''
    password = PasswordField()
    password_repeat = PasswordField(validate=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']


    def validate(self, data: dict) -> dict:
        '''
        Проверка совпадения введенного пароля и повторенного пароля
        '''
        password = data.get('password')
        password_repeat = data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data: dict) -> User:
        '''
        Шифрование пароля и создание нового пользователя
        '''
        validated_data['password'] = make_password(
            validated_data['password']
        )
        return User.objects.create(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для аутентификации пользователя
    '''
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data: dict):
        '''
        Проверка введенных данных и выполнение аутентификации.
        '''
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для отображения профиля пользователя
    '''
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class UserChangePasswordSerializer(serializers.Serializer):
    '''
    Сериализатор для смены пароля
    '''
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value: str) -> str:
        '''
        Проверка правильности ввода старого пароля
        '''
        user = self.context['request'].user
        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError("Wrong password.")
        return value

    def validate_new_password(self, value: str) -> str:
        '''
        Проверка несовпадения нового пароля со старым
        '''
        user = self.context['request'].user
        if user.check_password(value):
            raise serializers.ValidationError("New password must be different with the old password.")
        return value

    def update(self, instance, validated_data):
        '''
        Шифрование нового пароля и замена пароля.
        '''
        new_password = validated_data['new_password']
        instance.password = make_password(new_password)
        instance.save()
        return instance
