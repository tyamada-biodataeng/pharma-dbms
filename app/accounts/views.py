from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from accounts.forms import UserLoginForm


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/index.html'


class UserLoginView(LoginView):

    form_class = UserLoginForm
    template_name = 'accounts/login.html'


class UserLogoutView(LogoutView):
    pass
