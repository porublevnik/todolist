from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer
from core.models import User


class UserRegistrationView(CreateAPIView):
    '''
    Представление для регистрации нового пользователя.
    '''
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserLoginView(CreateAPIView):
    '''
    Представление для аутентификации нового пользователя.
    '''
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        '''
        Обрабатывает POST-запрос для выполнения входа пользователя.
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    '''
    Представление для просмотра, обновления профиля пользователя и выхода пользователя
    '''
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self) -> User:
        '''
        Возврат текущего пользователя
        '''
        return self.request.user

    def destroy(self, request, *args, **kwargs) -> Response:
        '''
        Выход пользователя из системы
        '''
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserChangePasswordView(UpdateAPIView):
    '''
    Представление для смены пароля
    '''
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        '''
        Возврат текущего пользователя
        '''

        return self.request.user
