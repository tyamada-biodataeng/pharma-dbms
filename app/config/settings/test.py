from .dev import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME', default='postgres'),
        'USER': f'{env("DATABASE_USER")}_test',
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST', default='postgres'),
        'PORT': env('DATABASE_PORT', default='5432'),
        'OPTIONS': {'options': f'-c search_path=test_{env("DATABASE_SCHEMA", default="public")},public'},
    }
}
