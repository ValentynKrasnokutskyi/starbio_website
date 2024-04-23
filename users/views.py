from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


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

# def register(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # creating an object without saving it to the DB
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})
