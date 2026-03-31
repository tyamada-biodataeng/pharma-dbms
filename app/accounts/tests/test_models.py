import pytest
from django.db import IntegrityError

from accounts.models import CustomUser


class TestCustomUser:
    def test_create_user(self, user):
        assert user.check_password('password')
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self, super_user):
        assert super_user.check_password('password')
        assert super_user.is_active
        assert super_user.is_staff
        assert super_user.is_superuser

    def test_soft_delete_deactivates_user(self, user):
        user.soft_delete()
        user.refresh_from_db()

        assert user.deleted_at is not None
        assert not user.is_active

    def test_restore_reactivates_user(self, user):
        user.soft_delete()
        user.restore()
        user.refresh_from_db()

        assert user.deleted_at is None
        assert user.is_active

    @pytest.mark.django_db
    def test_username_cannot_be_reused_after_soft_delete(self):
        user = CustomUser.objects.create_user(
            username='duplicate-user',
            email='first@example.com',
            password='password',
        )
        user.soft_delete()

        with pytest.raises(IntegrityError):
            CustomUser.objects.create_user(
                username='duplicate-user',
                email='second@example.com',
                password='password',
            )
