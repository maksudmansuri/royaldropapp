"""
Django settings for eca project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import django_heroku
import dj_database_url 
# import decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oa$c14fx9h-axyl0f%9+ij)(m35$0axixug)8&+)znm!mi689j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'


ALLOWED_HOSTS = ['royaldrop.herokuapp.com','127.0.0.1']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'front',
    'ecaadmin',
    'crispy_forms',
    'ckeditor', 
    'ckeditor_uploader',
    'accounts',
    # 'simple_email_confirmation',
    # 'moviepy',
    'django.contrib.humanize',
    # 'channels',
    'rest_framework',
    'rest_framework.authtoken',
    # 'social_django',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'accounts.LoginCheckMiddleWare.LoginCheckMiddleWare',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'eca.urls'

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
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'front.context_processors.basket',
            ],
        },
    },
]

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
 
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
 
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

REST_FRAMWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly'
        'rest_framework.permissions.IsAuthenticated'
        #  'rest_framework.permissions.IsAdminUser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'knox.auth.TokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'accounts.EmailBackEnd.EmailBackEnd',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10,
    # 'REST_SESSION_LOGIN' : False
   
}
CORS_ORIGIN_WHITELIST = (
    'localhost:1234',
)

# AUTHENTICATION_BACKENDS=(
#     'accounts.userAuthenticate.userAuthenticate',
#     # 'allauth.account.auth_backends.AuthenticationBackend',
# )


WSGI_APPLICATION = 'eca.wsgi.application'

# ASGI_APPLICATION = 'eca.routing.application'

AUTH_USER_MODEL="accounts.CustomUser"
# AUTH_USER_MODEL = 'accounts.User'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


LOGIN_URL='dologin'
LOGOUT_URL = 'dologout'

# LOGIN_REDIRECT_URL = "/"

# from datetime import timedelta
# REST_KNOX = {
#     'USER_SERIALIZER' : 'accounts.serializer.UserSerializer',
#     # 'TOKEN_TTL' : timedelta(hours=24),
#     'TOKEN_TTL': timedelta(hours=10),
#     # 'EXPIRY_DATETIME_FORMAT': api_settings.DATETME_FORMAT,
# }



CRISPY_TEMPLATE_PACK = 'bootstrap4'
# TEMP = os.path.join(BASE_DIR, "temp")

# LOGIN_URL = 'login'

# LOGIN_REDIRECT_URL = 'home'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE':'django.db.backends.mysql',
        'NAME':'ecomerceapp',
        'USER':'root',
        'PASSWORD':'Aot567@lk',
        'HOST':'localhost',
        'PORT':'3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

MEDIA_URL = "/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"media")

STATIC_URL = "/static/"
STATIC_ROOT=os.path.join(BASE_DIR,"static")

BASE_URL="http://127.0.0.1:8000"
# Manualy Added
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]

STATICFILE_STORAGE = "whitenoise.storage.CompressedMainfestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'intellecttec@gmail.com'
EMAIL_HOST_PASSWORD = 'Aot567{LK}'
EMAIL_USE_TLS = True

django_heroku.settings(locals())

from datetime import timedelta

EMAIL_CONFIRMATION_PERIOD_DAYS = 1
SIMPLE_EMAIL_CONFIRMATION_PERIOD = timedelta(days=EMAIL_CONFIRMATION_PERIOD_DAYS)
