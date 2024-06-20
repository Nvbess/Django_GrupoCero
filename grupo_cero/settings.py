"""
Django settings for grupo_cero project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%8fzd%$jl2rk7919qwtfv!zevr^$*0xh-%p38w-0)o7$!g0(%v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'admin_confirm',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'crispy_forms',
    'crispy_bootstrap4',
    'rest_framework',
    'axes',
    'captcha',
    'django_recaptcha',
    'cloudinary',
]

# KEYS DEL RECAPTCHA
RECAPTCHA_PUBLIC_KEY = '6LezsvUpAAAAAE65YuqsMpbqa3CY1SpLZCaLUko3'
RECAPTCHA_PRIVATE_KEY = '6LezsvUpAAAAANtRZBx5pB2wCefVhIRtmg5HCJpG'

X_FRAME_OPTIONS = "SAMEORIGIN"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware'
]

# CONFIGURACION AXES
AXES_FAILURE_LIMIT = 3                      #Numero de intentos fallidos.
AXES_COOLOFF_TIME = timedelta(minutes=1)    #Tiempo de espera antes de permitir otro intento.
AXES_LOCKOUT_URL = '/account_locked/'       #Ruta URL a la que se redirigue cuando la cuenta se bloquea.
AXES_RESET_ON_SUCCESS = True                #Reestablecemos el contador de intentos fallidos, cuando se logea correctamente.

# CONFIGURACION PAYPAL
PAYPAL_RECEIVER_EMAIL = 'sb-bpbsx31159923@business.example.com'
PAYPAL_TEST = True  # Cambia a False en producción

ROOT_URLCONF = 'grupo_cero.urls'

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

WSGI_APPLICATION = 'grupo_cero.wsgi.application'

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#CONFIG CLOUDINARY
CLOUDINARY_STORAGE = {
    'CLOUD_NAME' : 'dyh1syxfx',
    'API_KEY': '124746648463112',
    'API_SECRET':'YXbkHXnqiK45L71nXkMz66mnILo'
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'aws-0-sa-east-1.pooler.supabase.com',
        'NAME': 'postgres',
        'USER': 'postgres.odrompjyljvaatrdubwj',
        'PASSWORD': 'Grupocero@cero',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesStandaloneBackend',
    'core.backends.CaseInsensitiveModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

#CONFIGURACION LOGIN Y LOGOUT

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

#CONFIGURACION PARA LAS IMAGENES
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/' 



