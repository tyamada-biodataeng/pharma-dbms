from factory import LazyAttribute, post_generation
from factory.django import DjangoModelFactory

from accounts.models import CustomUser


class UserFactory(DjangoModelFactory):

    username = 'user'
    email = LazyAttribute(lambda u: f'{u.username}@example.com')
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = CustomUser
        django_get_or_create = ('username',)
        skip_postgeneration_save = True

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or 'password'
        self.set_password(password)
        if create:
            self.save()


class SuperUserFactory(UserFactory):

    username = 'superuser'
    is_staff = True
    is_superuser = True
