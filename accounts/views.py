# -*- coding: utf-8 -*-
"""Views for accounts."""

from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from accounts.models import TodoUser
from accounts.serializers import UserSerializer


class UserViewset(CreateModelMixin, UpdateModelMixin, GenericViewSet):  # noqa: D101
    queryset = TodoUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
