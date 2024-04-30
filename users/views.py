"""
Views for user authentication, registration, profile management, and password change.

These views handle user authentication, registration, updating user profile, and changing user password.
"""
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from starbio import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    """
    Class-based view for user login.

    Attributes:
        form_class (Form): Form for user authentication.
        template_name (str): Path to the template for login page.
        extra_context (dict): Additional context data for rendering the login page.
    """
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Authorization"}

    # def get_success_url(self):
    #     return reverse_lazy('home')


class RegisterUser(CreateView):
    """
   Class-based view for user registration.

   Attributes:
       form_class (Form): Form for user registration.
       template_name (str): Path to the template for registration page.
       extra_context (dict): Additional context data for rendering the registration page.
       success_url (str): URL to redirect to after successful registration.
   """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Registration"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    """
        Class-based view for user profile management.

        Attributes:
            model (Model): User model.
            form_class (Form): Form for updating user profile.
            template_name (str): Path to the template for user profile page.
            extra_context (dict): Additional context data for rendering the user profile page.
        """
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "User profile",
                     'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """
        Class-based view for changing user password.

        Attributes:
            form_class (Form): Form for changing user password.
            success_url (str): URL to redirect to after successful password change.
            template_name (str): Path to the template for password change page.
            extra_context (dict): Additional context data for rendering the password change page.
        """
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Changing your password"}
