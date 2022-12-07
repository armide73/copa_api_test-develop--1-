"""
Django settings for copa project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import cloudinary

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name="julien",
    api_key="929323731828174",
    api_secret="NL1a-DkhIWSgGw5DmHCMqeNaIvY",
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "22(ln1b1hq#_+jo40rok@2l43n_(xzki7%+#4n6kxx*7aao+@1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", True)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "graphene_django",
    "cloudinary",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    # 'django_ledger',
    "copa.apps.authentication",
    "copa.apps.cooperative",
    "copa.apps.stock",
    "copa.apps.pricing",
    "copa.apps.spenn",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "copa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "copa.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "copa"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "armide"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# GraphQl settings
GRAPHENE = {
    "SCHEMA": "copa.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        "graphene_django.debug.DjangoDebugMiddleware",
        "graphene_django_extras.ExtraGraphQLDirectiveMiddleware",
    ],
    "SCHEMA_INDENT": 4,
}

GRAPHENE_DJANGO_EXTRAS = {
    "DEFAULT_PAGINATION_CLASS": "graphene_django_extras.paginations.LimitOffsetGraphqlPagination",
    "DEFAULT_PAGE_SIZE": 20,
    "MAX_PAGE_SIZE": 100,
    "CACHE_ACTIVE": True,
    "CACHE_TIMEOUT": 300,  # seconds
}

# Add settings for authentication with graphql_jwt
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Define global variables
AUTH_USER_MODEL = "authentication.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "copa/static/")]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

CORS_ORIGIN_ALLOW_ALL = True

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


KUDIBOOKS_API_URL = os.environ.get("KUDIBOOKS_API_URL", "http://178.62.123.99/api/v1")
KUDIBOOKS_API_KEY = os.environ.get(
    "KUDIBOOKS_API_KEY", "7|o6M1ceg0KrBsEY5ttcbhf0Ya0o7JFORwIUgUFxp1"
)

SPENN_API_KEY = os.environ.get("SPENN_API_KEY", "")
SPENN_CLIENT_ID = os.environ.get("SPENN_CLIENT_ID")
SPENN_CLIENT_SECRET = os.environ.get("SPENN_CLIENT_SECRET")
SPENN_AUTH_API_URL = os.environ.get("SPENN_AUTH_API_URL", "")
SPENN_PARTNER_API_URL = os.environ.get("SPENN_PARTNER_API_URL")
SPENN_CALLBACK_URL = os.environ.get("SPENN_CALLBACK_URL", "")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
