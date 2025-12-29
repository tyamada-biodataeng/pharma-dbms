from django.urls import path

from accounts.views import IndexView, UserLoginView, UserLogoutView

app_name = 'accounts'
urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='index'),
]
