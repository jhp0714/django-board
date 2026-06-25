from .base import *

ALLOWED_HOSTS = ['3.36.39.13', 'boardhj.kro.kr', 'www.boardhj.kro.kr']

DEBUG = False

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}