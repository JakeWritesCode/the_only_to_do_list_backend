# -*- coding: utf-8 -*-
"""Serializers for Accounts app."""

from rest_framework import serializers

from accounts.models import TodoUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return TodoUser.objects.create(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.password = validated_data.get("password", instance.password)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance

    class Meta:
        model = TodoUser
        fields = ("id", "email", "password", "first_name", "last_name")
