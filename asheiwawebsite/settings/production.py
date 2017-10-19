"""
Django settings for asheiwawebsite project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os, re

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^2!f*(e3=#2$kch$bgd4f4vhme8b$*(hm@a!r@c8860l^-ire$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['asheiwawebsite.herokuapp.com','127.0.0.1','asheiwa.pythonanywhere.com']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'afip.hidayatulloh@gmail.com'
EMAIL_HOST_PASSWORD = 'th1s1ssp4rt445'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    'crispy_forms',
    'markdown_deux',
    'pagedown',
    # local apps
    'posts',
    'comments'
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MARKDOWN_DEUX_STYLES = {
    # Here is what http://code.activestate.com/recipes/ currently uses.
    "recipe": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": "escape",
        "link_patterns": [
            # Transform "Recipe 123" in a link.
            (re.compile(r"recipe\s+#?(\d+)\b", re.I),
             r"http://code.activestate.com/recipes/\1/"),
        ],
        "extras": {
            "code-friendly": None,
            "pyshell": None,
            "demote-headers": 3,
            "link-patterns": None,
            # `class` attribute put on `pre` tags to enable using
            # <http://code.google.com/p/google-code-prettify/> for syntax
            # highlighting.
            "html-classes": {"pre": "prettyprint"},
            "cuddled-lists": None,
            "footnotes": None,
            "header-ids": None,
        },
        "safe_mode": "escape",
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'asheiwawebsite.urls'

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

WSGI_APPLICATION = 'asheiwawebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
                os.path.join(BASE_DIR, "static"),
            ]
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")
MEDIA_ROOT = os.path.join( os.path.dirname(BASE_DIR), "media_cdn")
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage' 

'''
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
]

STATIC_ROOT = os.path.join( os.path.dirname(BASE_DIR), "static_cdn")
MEDIA_ROOT = os.path.join( os.path.dirname(BASE_DIR), "media_cdn")
'''

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# post settings
category_choices = (
        ('ATW', 'Artworks'),
        ('PGT', 'Project'),
        ('RGN', 'Rigging'),
        ('SCT', 'Scripting'),
        ('MDL', 'Modeling'),
        ('TRL', 'Tutorial'),
        ('OTH', 'Other')
    )