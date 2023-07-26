from django.urls import path

from core import views

urlpatterns = [
    path('signup', views.UserRegistrationView.as_view(), name='signup'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('update_password', views.UserChangePasswordView.as_view(), name='user-profile'),
]