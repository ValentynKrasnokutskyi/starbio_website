from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    """
        Custom authentication backend for authenticating users using email addresses.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()  # Get the user model
        try:
            user = user_model.objects.get(email=username)  # Retrieve user by email
            if user.check_password(password):  # Check if password is correct
                return user  # Return user if authentication succeeds
            return None  # Return None if password is incorrect
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None  # Return None if user is not found or multiple users found

    def get_user(self, user_id):
        """
            Retrieve a user by user ID.
        """
        user_model = get_user_model()  # Get the user model
        try:
            return user_model.objects.get(pk=user_id)  # Retrieve user by primary key
        except user_model.DoesNotExist:
            return None  # Return None if user is not found
