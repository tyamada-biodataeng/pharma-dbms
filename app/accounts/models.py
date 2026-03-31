from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import CustomBaseModel, SoftDeleteQuerySet


class CustomUserQuerySet(SoftDeleteQuerySet):
    def soft_delete(self):
        now = timezone.now()
        return self.update(deleted_at=now, updated_at=now, is_active=False)

    def restore(self):
        return self.update(deleted_at=None, updated_at=timezone.now(), is_active=True)


class CustomUserManager(BaseUserManager.from_queryset(CustomUserQuerySet)):
    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset().alive()

    def with_deleted(self):
        return super().get_queryset()

    def create_user(self, username, email, password=None):

        if not username:
            raise ValueError('Users must have a username.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(CustomBaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name=_('username'), max_length=20, unique=True)
    email = models.EmailField(verbose_name=_('email address'), max_length=254, blank=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('staff'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'email',
    ]

    def save(self, **kwargs):
        if self.deleted_at is not None:
            self.is_active = False
        super().save(**kwargs)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save(update_fields=['deleted_at', 'is_active', 'updated_at'])

    def restore(self):
        self.deleted_at = None
        self.is_active = True
        self.save(update_fields=['deleted_at', 'is_active', 'updated_at'])

    def __str__(self):
        return self.username
