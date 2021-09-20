# -*- coding: utf-8 -*-
"""Models for accounts app."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class TodoUser(AbstractUser):
    """Extend the standard user model."""

    # Email should be username, everyone hates usernames
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self):  # noqa: D105
        return f"{self.first_name} {self.last_name} - {self.email}"
