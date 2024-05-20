from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    def setUp(self):
        # Data to be used for user registration tests
        self.data = {
            "username": "user_1",
            "email": "user_1@starbio.com",
            "first_name": "Valentyn",
            "last_name": "Krasnokutskyi",
            "password1": "12345678Aa",
            "password2": "12345678Aa",
        }

    def test_form_registration_get(self):
        # Test GET request to the registration page
        path = reverse("users:register")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register.html")

    def test_user_registration_success(self):
        # Test successful user registration
        user_model = get_user_model()

        path = reverse("users:register")
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # Redirect status after successful registration
        self.assertRedirects(response, reverse("users:login"))  # Check redirect to login page
        self.assertTrue(user_model.objects.filter(username=self.data["username"]).exists())  # Verify user creation

    def test_user_registration_password_error(self):
        # Test registration failure due to password mismatch
        self.data["password2"] = "12345678A"  # Mismatched password
        path = reverse("users:register")
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Should return OK with the form re-rendered
        self.assertContains(response, "The two password fields didn’t match")  # Check error message

    def test_user_registration_user_exists_error(self):
        # Test registration failure due to existing username
        user_model = get_user_model()
        user_model.objects.create(username=self.data["username"])  # Create user with same username

        path = reverse("users:register")
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Should return OK with the form re-rendered
        self.assertContains(response, "A user with that username already exists.")  # Check error message
