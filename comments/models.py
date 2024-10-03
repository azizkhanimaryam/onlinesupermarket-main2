from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import CustomUser


def get_default_user():
    User = get_user_model()  # This gets the user model defined in settings.AUTH_USER_MODEL

    try:
        return User.objects.get(pk=1).id
    except User.DoesNotExist:
        # Handle the case where the default user does not exist
        return None

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)  # Allow user to be null
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username if self.user else "Unknown"} on {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
