from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    """
    A form for authenticating users.
    """
    username = forms.CharField(label='Login',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    """
    A form for registering new users.
    """
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'First name',
            'last_name': 'Last name',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        """
        Checking the uniqueness of Email
        """
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This E-mail already exists!")
        return email


class ProfileUserForm(forms.ModelForm):
    """
    A form for updating user profile information.
    """
    username = forms.CharField(disabled=True, label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5))))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    """
    A form for changing user password.
    """
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Password confirmation",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
