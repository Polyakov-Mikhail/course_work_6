from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserResetPasswordView, UserForgotPasswordView, \
    UserPasswordResetConfirmView, ProfileView, user_list, toggle_activation

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path("email_confirm/<str:token>/", email_verification, name='email-confirm'),
    path('reset-password/', UserResetPasswordView.as_view(), name='reset_password'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', user_list, name='user_list'),
    path('toggle/<int:user_id>/', toggle_activation, name='toggle_activation'),
]
