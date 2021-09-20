# -*- coding: utf-8 -*-
"""Serializers for Accounts app."""

import django.contrib.auth.password_validation as password_validator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from accounts.models import TodoUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the TodoUser model."""

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):  # noqa: D102
        user = TodoUser(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.password = make_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):  # noqa: D102
        instance.email = validated_data.get("email", instance.email)
        try:
            password = validated_data.get("password")
            instance.password = make_password(password)
        except KeyError:
            pass
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance

    def validate(self, data):  # noqa: D102
        errors = dict()
        password = data.get("password")
        user = TodoUser(**data)

        try:
            password_validator.validate_password(password=password, user=user)
        except ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    class Meta:  # noqa: D106
        model = TodoUser
        fields = ("id", "email", "password", "first_name", "last_name")
