from django.contrib.auth.views import LoginView

from accounts.forms import UserLoginForm


class UserLoginView(LoginView):

    form_class = UserLoginForm
    template_name = 'accounts/login.html'
