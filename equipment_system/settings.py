"""
Django settings for equipment_system project.
"""

from pathlib import Path
import os

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY

SECRET_KEY = 'django-insecure-your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []



# APPLICATIONS

INSTALLED_APPS = [
    "jazzmin",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # MY APPS
    'accounts',
    'core',
    'equipment',
    'borrow',
]



# MIDDLEWARE

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



# ROOT URL

ROOT_URLCONF = 'equipment_system.urls'



# TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # GLOBAL TEMPLATES FOLDER
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        # APP TEMPLATES ENABLED
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                
                # NOTIFICATION CONTEXT PROCESSOR
                
                'borrow.context_processors.unread_notifications',
            ],
        },
    },
]


WSGI_APPLICATION = 'equipment_system.wsgi.application'



# DATABASE (MYSQL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'equipment_system',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}



# PASSWORD VALIDATION

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]



# INTERNATIONALIZATION

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True



# STATIC FILES

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



# DEFAULT PRIMARY KEY

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# LOGIN SETTINGS

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'



# STATIC FILE FINDERS

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]



# JAZZMIN CONFIG

JAZZMIN_SETTINGS = {
    "site_title": "Equipment System",
    "site_header": "Equipment Admin",
    "site_brand": "Equipment System",
    "welcome_sign": "Welcome to Dashboard",

    # REMOVE FOOTER
    "show_footer": False,

    "show_sidebar": True,
    "navigation_expanded": True,

    # MODAL UI ENHANCEMENT
    "related_modal_active": True,
}