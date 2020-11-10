"""
Django settings for astigmia project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import configparser
from datetime import timedelta
import os
from pathlib import Path

import django_heroku

# Import sensitive configuration from an INI file
config = configparser.ConfigParser()
config.read('astigmia/config.ini')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'lobby.apps.LobbyConfig',
    'dashboard.apps.DashboardConfig',
    'meals.apps.MealsConfig',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

ROOT_URLCONF = 'astigmia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'astigmia/templates/shared'),
        ],
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

WSGI_APPLICATION = 'astigmia.wsgi.application'

# Authentication overrides
# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#authentication-backends

AUTHENTICATION_BACKENDS = [
    'lobby.auth_backend.MyVisionBackend'
]

AUTH_USER_MODEL = 'lobby.user'

LOGIN_REDIRECT_URL = '/dashboard'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# TODO: Probably hook this up to a PostgreSQL instance

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
"""
For now, we only have one user so no value in having eg; an nginx instance caching static assets
Also, given we're currently on Heroku, I'm not sure this has much value as a setting re: pointing
at the filesystem
"""
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = []

# MyVision settings (check env first followed by config for local dev)
MV_USERNAME = os.getenv('MV_USERNAME')
MV_PASSWORD = os.getenv('MV_PASSWORD')
MV_API_BASE = os.getenv('MV_API_BASE')

# Celery (mostly recommended settings from https://www.cloudamqp.com/docs/celery.html)
CELERY_BEAT_SCHEDULE = {
    'check-next-session': {
        'task': 'dashboard.tasks.check_next_session',
        'schedule': timedelta(hours=3)
    },
    'fetch-notifications': {
        'task': 'dashboard.tasks.fetch_notifications',
        'schedule': timedelta(hours=3)
    },
    'update-goals': {
        'task': 'dashboard.tasks.update_targets_and_goals',
        'schedule': timedelta(hours=12)
    },
}
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_CONNECTION_TIMEOUT = 30
CELERY_BROKER_POOL_LIMIT = 1
CELERY_BROKER_URL = os.getenv('CLOUDAMQP_URL', 'amqp://localhost')
CELERY_BROKER_HEARTBEAT = None
CELERY_RESULTS_BACKEND = 'django-db'
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_TRACK_STARTED = True
CELERY_TIMEZONE = 'Pacific/Auckland'
CELERYD_CONCURRENCY = 50
CELERYD_PREFETCH_MULTIPLIER = 1

# Enable django-heroku (always keep this at the bottom)
django_heroku.settings(locals())
