"""
Django settings for helfa_aux_dev project.
"""

from pathlib import Path
import os
from creds_my import mysql_pw
from env import DATABASE_NAME, ENV #, ALLOWED_HOSTS
from env import TELEGRAM_BOT_NAME, TELEGRAM_BOT_TOKEN, TELEGRAM_LOGIN_REDIRECT_URL, TELEGRAM

ALLOWED_HOSTS = [
'helfa-augsburg.ddnss.de',
'helfa99.loca.lt',
'localhost',
]

CSRF_TRUSTED_ORIGINS = [
'https://helfa99.loca.lt',
'https://helfa-augsburg.ddnss.de',
]
#CSRF_COOKIE_SECURE = False
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

MAX_LENGTH = 35

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_NAME = 'helfa_aux_dev'

if ENV=='prod':
  FORCE_SCRIPT_NAME = '/dj/'
  #FORCE_SCRIPT_NAME = '/dj'
  TMPPATH = '/var/www/django/helfa_aux/tmp'
elif ENV=='dev':
  FORCE_SCRIPT_NAME = '/'
  TMPPATH = '/var/tmp/'+BASE_NAME
else:
  raise ValueError("ENV not set")

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
    'mptt',
    'django_tgbot',
    'helfa_aux_dev_bot',
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
        'DIRS': [ os.path.join(BASE_DIR, 'templates'),
                  os.path.join(BASE_DIR, 'djflow/templates'),
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
    '/var/www/django/helfa_aux/static'
]

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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_debug,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
