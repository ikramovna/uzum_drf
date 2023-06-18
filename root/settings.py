import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

load_dotenv()

ALLOWED_HOSTS = ['*']

MY_APPS = [
    'apps.users',
    'apps.products',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_yasg',
    'mptt',
    'parler',
    'django_filters',

]

INSTALLED_APPS = [
                     'modeltranslation',
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',

                 ] + MY_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'root.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.accounts.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.accounts.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.accounts.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.accounts.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
    ('uz', 'Uzbek'),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')

MODELTRANSLATION_LANGUAGES = ('ru', 'en', 'uz')
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Cache Config

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# DRF Config

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}
