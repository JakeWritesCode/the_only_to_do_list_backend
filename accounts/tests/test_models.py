from django.test.testcases import TestCase
from ..models import TodoUser


class TodoUserTests(TestCase):
    def test_user_can_be_created_without_username(self):
        """Should be able to create a user without username"""
        TodoUser.objects.create(
            email="test@user.com",
            first_name="Test",
            last_name="User",
            password="Hellothere!",
        )
        assert TodoUser.objects.all().count() == 1

    def test_str(self):
        """Test string representation of model instnace"""
        TodoUser.objects.create(
            email="test@user.com",
            first_name="Test",
            last_name="User",
            password="Hellothere!",
        )
        assert str(TodoUser.objects.first()) == "Test User - test@user.com"
