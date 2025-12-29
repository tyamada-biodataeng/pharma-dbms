from factory import LazyAttribute
from factory.django import DjangoModelFactory

from accounts.models import CustomUser


class UserFactory(DjangoModelFactory):

    username = 'user'
    email = LazyAttribute(lambda u: f'{u.username}@example.com')
    password = 'password'
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = CustomUser
        django_get_or_create = ('username',)


class SuperUserFactory(UserFactory):

    username = 'superuser'
    is_staff = True
    is_superuser = True
