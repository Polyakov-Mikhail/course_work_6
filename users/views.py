import secrets
import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.forms import BooleanField
from django.core.exceptions import PermissionDenied
from django.contrib import messages


from users.forms import UserRegisterForm, ResetPasswordForm, UserForgotPasswordForm, UserSetNewPasswordForm, UserProfileFrom
from users.models import User

from config.settings import EMAIL_HOST_USER


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}'
        send_mail(
            subject="Подтверждение почты",
            message=f"Необходимо перейти по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserResetPasswordView(PasswordResetView, StyleFormMixin):
    """
    Сброс пароля с использованием email
    """
    form_class = ResetPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Проверяет валидность и сохраняет новый пароль
        """
        email = form.cleaned_data['email']
        # Проверяем наличие пользователя с указанной почтой
        try:
            user = User.objects.get(email=email)
            if user:
                # Создаем новый пароль для пользователя и отправляем его на почту
                password = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
                user.set_password(password)
                user.is_active = True
                user.save()
                send_mail(
                    subject='Сброс пароля',
                    message=f'Новый пароль: {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
            return redirect(reverse('users:login'))
        except User.DoesNotExist:
            # Если пользователь не найден, перенаправляем на страницу регистрации
            return redirect(reverse('users:register'))


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Cброс пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileFrom
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def user_list(request):
    user = request.user
    if user.is_authenticated and user.groups.filter(name='manager').exists():
        users = User.objects.all()
        return render(request, 'users/user_list.html', {'users': users})
    raise PermissionDenied


def toggle_activation(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()

    action = 'активирован' if user.is_active else 'деактивирован'
    messages.success(request, f'Пользователь {user.email} был {action}.')

    return redirect('users:user_list')  # Перенаправляем обратно в список пользователей
