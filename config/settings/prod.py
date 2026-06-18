from .base import *

ALLOWED_HOSTS = ['3.36.39.13','boardhj.kro.kr','www.boardhj.kro.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'board',
        'USER': 'dbmasteruser',
        'PASSWORD': '6V:0{KMDYx)c6H^G&PdiR{k.*1;EZgd)',
        'HOST': 'ls-e368986d13304641e3a0698314ca7aec99218605.crskikqoqlis.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}