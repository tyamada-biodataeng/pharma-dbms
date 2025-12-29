import pytest

from .factories import UserFactory, SuperUserFactory


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def users(db):
    return UserFactory.create_batch(5)


@pytest.fixture
def super_user(db):
    return SuperUserFactory()


@pytest.fixture
def super_users(db):
    return SuperUserFactory.create_batch(5)
