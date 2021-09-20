# -*- coding: utf-8 -*-
"""Admin for Accounts app."""

from django.contrib import admin

from accounts.models import TodoUser

admin.register(TodoUser)
