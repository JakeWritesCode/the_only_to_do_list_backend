# -*- coding: utf-8 -*-
"""Tests for accounts serializers."""

from unittest.mock import patch

from django.contrib.auth.hashers import check_password
from django.test import TestCase

from accounts.models import TodoUser
from accounts.serializers import UserSerializer


class UserSerializerTests(TestCase):
    """Tests for the user serializer."""

    def setUp(self) -> None:  # noqa: D102
        self.data = {
            "email": "myemail@test.com",
            "first_name": "Jake",
            "last_name": "Saunders",
            "password": "IAmANoodle",
        }

    def test_serialize(self):
        """Serializer should serialize a TodoUser correctly."""
        user = TodoUser.objects.create(
            email="myemail@test.com",
            first_name="Jake",
            last_name="Saunders",
        )
        serializer = UserSerializer(user)
        assert serializer.data == {
            "email": "myemail@test.com",
            "first_name": "Jake",
            "last_name": "Saunders",
            "id": user.id,
        }

    def test_validation_good_data(self):
        """Serializer should de-serialize a TodoUser correctly."""
        serializer = UserSerializer(data=self.data)
        serializer.is_valid()

        assert serializer.validated_data == self.data

    @patch("accounts.serializers.password_validator.validate_password")
    def test_validation_uses_django_password_validator(self, mock_validator):
        """Validation should use the django standard password validator."""
        serializer = UserSerializer(data=self.data)
        serializer.is_valid()

        mock_validator.assert_called_once()
        assert mock_validator.call_args[1]["password"] == "IAmANoodle"

    def test_password_validation_issues_are_passed_through(self):
        """Password validator errors should be passed through to the serializer as field errors."""
        self.data["password"] = "a"
        serializer = UserSerializer(data=self.data)
        is_valid = serializer.is_valid()
        test = 1
        assert not is_valid
        assert serializer.errors["password"] == [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common.",
        ]

    def test_create(self):
        """Test create method creates an instance correctly."""
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid()
        serializer.create(serializer.validated_data)

        instance = TodoUser.objects.first()
        assert instance.email == self.data["email"]
        assert instance.first_name == self.data["first_name"]
        assert instance.last_name == self.data["last_name"]
        assert check_password(password=self.data["password"], encoded=instance.password)

    def test_update(self):
        """Serializer method should mutate and save user."""
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid()
        serializer.create(serializer.validated_data)

        new_data = {
            "email": "new_email@test.com",
            "first_name": "Barry",
            "last_name": "White",
            "password": "CantGetEnoughOfYourLoveBaby",
        }

        instance = TodoUser.objects.first()
        serializer = UserSerializer(data=new_data)
        assert serializer.is_valid()
        serializer.update(instance, serializer.validated_data)
        instance.refresh_from_db()

        assert instance.email == "new_email@test.com"
        assert instance.first_name == "Barry"
        assert instance.last_name == "White"
        assert check_password("CantGetEnoughOfYourLoveBaby", instance.password)
