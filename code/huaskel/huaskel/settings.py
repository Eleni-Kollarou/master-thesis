"""
Django settings for huaskel project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import ldap
from django_auth_ldap.config import LDAPSearch
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DJANGO_PROJECT = os.getenv('DJANGO_PROJECT','huaskel')
DB_HOST = os.getenv('DB_HOST','db')
DB_NAME = os.getenv('DB_NAME','huaskel')
DB_USER = os.getenv('DB_USER','huaskel')
DB_PASSWORD = os.getenv('DB_PASSWORD','huaskel')
DEBUG = (os.getenv('DEBUG', 'True') == 'True')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@d%ay!8&l+6jh0@t7@qlw(+coi+-a-gz04)554yw%bm5728z*w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['accounts.ditapps.hua.gr', 'localhost']


# Application definition

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_ROOT = '/code/static'

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'attendances.apps.AttendancesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = DJANGO_PROJECT + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = DJANGO_PROJECT + '.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
	'USER': DB_USER,
	'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

print(LOCALE_PATHS)
LANGUAGES = (
    ('en', _('English')),
    ('el', _('Greek')),
)

LANGUAGE_CODE = 'el'

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/



AUTH_USER_MODEL = 'accounts.User'
#AUTHENTICATION_BACKENDS = ["django_auth_ldap.backend.LDAPBackend", "django.contrib.auth.backends.ModelBackend"]
AUTHENTICATION_BACKENDS = ["accounts.backends.EmailBackend","django_auth_ldap.backend.LDAPBackend"]
AUTH_LDAP_SERVER_URI = os.getenv('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = os.getenv('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.getenv('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_START_TLS = os.getenv('AUTH_LDAP_START_TLS') == 'True'
AUTH_LDAP_BASE_DN = os.getenv('AUTH_LDAP_BASE_DN')
AUTH_LDAP_USER_SEARCH_ATTR = os.getenv('AUTH_LDAP_USER_SEARCH_ATTR')
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_BASE_DN,
    ldap.SCOPE_SUBTREE,
    "(" + AUTH_LDAP_USER_SEARCH_ATTR + "=%(user)s)"
)
AUTH_LDAP_SN = os.getenv('AUTH_LDAP_SN')
AUTH_LDAP_EMAIL = os.getenv('AUTH_LDAP_EMAIL')
AUTH_LDAP_TITLE = os.getenv('AUTH_LDAP_TITLE')
AUTH_LDAP_DEPARTMENT = os.getenv('AUTH_LDAP_DEPARTMENT')
AUTH_LDAP_GIVEN_NAME = os.getenv('AUTH_LDAP_GIVEN_NAME')
AUTH_LDAP_USER_ATTR_MAP = {
  "first_name" : AUTH_LDAP_GIVEN_NAME,
  "last_name": AUTH_LDAP_SN,
  "email" : AUTH_LDAP_EMAIL,
  'department' : AUTH_LDAP_DEPARTMENT,
  'title' : AUTH_LDAP_TITLE
}
AUTH_LDAP_INTERNAL_DOMAIN = os.getenv('AUTH_LDAP_INTERNAL_DOMAIN')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose' : {
            'format' : '{asctime} {levelname} {message}',
            'style' : '{',
        },
    },
    'handlers': {
        'console' : {
            'class' : 'logging.StreamHandler',
           },
        'file' : {
            'class' : 'logging.FileHandler',
            'filename' : '/var/log/django_app.log',
            'formatter' : 'verbose'
        }
    },
    'loggers': {
        'django_auth_ldap': {
            'level': 'DEBUG',
            'handlers': ['file', 'console']
            },
        'huaskel' : {
            'level' : 'DEBUG',
            'handlers': ['file', 'console'],
            }
        }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/attendances/'

