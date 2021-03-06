#encoding:utf-8

"""
Django settings for hpm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c+c_bqsj0#txzk3_#@iz^h=e@8lm5r8qef-kh4s00zn3q4-gmf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'principal',
    'app_proyecto',
    'app_fase',
    'app_usuario',
    'app_rol',
    'app_comite',
    'app_tipo_item',
    'app_linea_base',
    'app_item',
    'app_mensajeria',
    'app_solicitud',
    'app_reporte',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hpm.urls'

WSGI_APPLICATION = 'hpm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

     # 'default': {
     #     'ENGINE':'django.db.backends.postgresql_psycopg2',
     #     'NAME': 'HPM',
     #     'USER': 'postgres',
     #     'PASSWORD': 'postgres',
     #     'HOST': '127.0.0.1',
     #     'PORT': '5432',
     # }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-PY'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

ADMINS = (
   ('Santiago Valdez', 'santiago.kenshinvaldez@gmail.com'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
MEDIA_URL = '/media/'