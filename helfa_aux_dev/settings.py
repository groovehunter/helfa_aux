"""
Django settings for helfa_aux_dev project.
"""

from pathlib import Path
import os
from creds_my import mysql_pw
from env import DATABASE_NAME #, ALLOWED_HOSTS
ALLOWED_HOSTS = [
  'helfaauxdev123.loca.lt',
'helfa99.loca.lt'
]
TELEGRAM_BOT_NAME = 'helfa_aux_dev_bot'
TELEGRAM_BOT_TOKEN = '5562362774:AAEQt9DXCvhzOhF639sd38hie7AfjRsvr18'
TELEGRAM_LOGIN_REDIRECT_URL = 'https://helfa99.loca.lt/users/tg_login'

#CSRF_TRUSTED_ORIGINS = 'https://'+ALLOWED_HOSTS[0]
CSRF_TRUSTED_ORIGINS = [
'https://helfaauxdev123.loca.lt',
'https://helfa99.loca.lt',
]
#CSRF_COOKIE_SECURE = False




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_NAME = 'helfa_aux_dev'
TMPPATH = '/var/tmp/'+BASE_NAME
LOG_DIR = TMPPATH + '/log'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h31p+=4b1boz(=(_g&6nz8#*1ljq7q22)qjm!z#9u^d+2-(yvd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG2 = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_telegram_login',
    'django_tables2',
    'users',
    'verschenka',
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


ROOT_URLCONF = 'helfa_aux_dev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'helfa_aux_dev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': DATABASE_NAME,
    'USER': 'django',
    'PASSWORD': mysql_pw,
  },
}

AUTH_USER_MODEL = 'users.CustomUser'
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/django/helfa_aux_dev/static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

### dev 

logfn_debug = LOG_DIR + '/debug.log'
logfn_piheat= LOG_DIR + '/piheat.log'
logfn_django= LOG_DIR + '/django.log'
logfn_root  = LOG_DIR + '/root.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname}| {module},{lineno} - {message}',
            'style': '{',
            'datefmt': '%H:%M:%S',
        },
        'simple': {
            'format': '{levelname}| {module} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_root': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_root,
            'formatter': 'verbose',
        },
        'file_django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_django,
            'formatter': 'simple',
        },
        'file_piheat': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_piheat,
            'formatter': 'verbose',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_debug,
            'formatter': 'verbose',
        },
       'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file_root'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['file_django'],
            'level': 'INFO',
            'propagate': False,
        },
        'motors.rules': {
            'handlers': ['file_piheat'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'motors.views': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'asyncio': { 'level': 'WARNING', },
        'faker.factory': { 'level': 'WARNING', },
    },
}

