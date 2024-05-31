from django.contrib.auth.models import Group


def new_users_handler(backend, user, response, *args, **kwargs):
    """
        Function to handle new users authenticated via social backend.
    """
    group = Group.objects.filter(name="social")
    if len(group):
        user.groups.add(group[0])
