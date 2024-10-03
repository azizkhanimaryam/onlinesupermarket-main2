from django.contrib.auth import get_user_model

def get_default_user():
    User = get_user_model()  # This gets the user model defined in settings.AUTH_USER_MODEL
    try:
        return User.objects.get(pk=1).id  # Adjust '1' if the default user ID is different
    except User.DoesNotExist:
        return None
