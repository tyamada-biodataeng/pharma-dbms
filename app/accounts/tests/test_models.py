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
