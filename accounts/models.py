from django.contrib.auth.models import AbstractUser
from django.db import models


class TodoUser(AbstractUser):
    """Extend the standard user model."""

    # Email should be username, everyone hates usernames
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
