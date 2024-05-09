from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Spouse, Stars

import re


class AddPostForm(forms.ModelForm):  # Form for adding a new post
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Category not selected', label='Category')
    spouse = forms.ModelChoiceField(queryset=Spouse.objects.all(), empty_label='Single', required=False, label='Spouse')

    class Meta:  # Meta class defining form behavior
        model = Stars  # Model associated with the form

        # Fields to include in the form
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'spouse', 'tags']

        labels = {'slug': 'URL'}  # Custom labels for form fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }  # Custom widgets for form fields

    def clean_title(self):
        title = self.cleaned_data['title']  # Retrieve the cleaned title from form data

        # Regular expression to match allowed characters
        ALLOWED_CHARS = r'^(?!.*--)(?!.*\s-$)(?!^\s)(?!^-)[a-zA-Zа-яА-Я \-]+(?<!-)$'

        if not re.match(ALLOWED_CHARS, title):  # Check if the title matches the allowed characters pattern
            # Raise a validation error if the title format is invalid
            raise ValidationError("Must only contain alphabetic characters, hyphen and space or invalid input format!")

        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Image")


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
