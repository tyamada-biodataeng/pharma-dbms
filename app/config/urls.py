"""
URL configuration for config project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from ninja import NinjaAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == 'supersecret':
            return token

if settings.DEBUG:
    api_title = 'Pharma DBMS dev API'
else:
    api_title = 'Pharma DBMS API'

api = NinjaAPI(
    title=api_title,
    version='1.0.0',
    auth=GlobalAuth(),
    docs_decorator=login_required,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path('', include('accounts.urls')),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += debug_toolbar_urls()
