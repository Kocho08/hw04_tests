from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordChange(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:password_change_done')
    template_name = 'users/password_change_form.html'


class PasswordReset(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:password_reset_done')
    template_name = 'users/password_reset_form.html'


class PasswordResetConfirm(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:password_reset_complete')
    template_name = 'users/password_reset_confirm.html'


class PasswordResetComplete(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:password_reset_complete')
    template_name = 'users/password_reset_confirm.html'
