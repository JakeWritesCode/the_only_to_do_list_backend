# -*- coding: utf-8 -*-
"""URLs for project."""

from rest_framework.routers import DefaultRouter
from .views import UserViewset

urlpatterns = []


router = DefaultRouter()
router.register(r"users", UserViewset, basename="user")
urlpatterns += router.urls
