"""
Django settings for nekos_api project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from pathlib import Path

from datetime import timedelta

import os

import grequests

import dotenv

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# Application definition

INSTALLED_APPS = [
    # Daphne
    "daphne",
    # Django Admin Interface
    "admin_interface",
    "colorfield",
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Nekos API Apps
    "api.apps.ApiConfig",
    "artists.apps.ArtistsConfig",
    "categories.apps.CategoriesConfig",
    "characters.apps.CharactersConfig",
    "images.apps.ImagesConfig",
    "lists.apps.ListsConfig",
    "users.apps.UsersConfig",
    "users.sso.apps.SsoConfig",
    "applications.apps.ApplicationsConfig",
    "webhooks.apps.WebhooksConfig",
    "gifs.apps.GifsConfig",
    # Third party apps
    "rest_framework",
    "oauth2_provider",
    "django_hosts",
    "django_ratelimit",
    "django_resized",
    "django_cleanup.apps.CleanupConfig",
    "django_bunny",
    "logentry_admin",
    "thumbnails",
]

MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "nekos_api.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "nekos_api.middleware.DisableCSRFMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    # "api.middleware.JSONAPIMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
]

ROOT_URLCONF = "nekos_api.urls"
ROOT_HOSTCONF = "nekos_api.hosts"

DEFAULT_HOST = "admin" if not DEBUG else "api"

SITE_ID = 1

SESSION_COOKIE_DOMAIN = os.getenv("BASE_DOMAIN")

DJANGORESIZED_DEFAULT_SIZE = None
DJANGORESIZED_DEFAULT_SCALE = None
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "WEBP"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"WEBP": ".webp"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = False

THUMBNAILS = {
    "METADATA": {
        "PREFIX": "thumbs",
        "BACKEND": "thumbnails.backends.metadata.RedisBackend",
        "db": 0,
        "port": int(os.getenv("REDIS_PORT")),
        "host": os.getenv("REDIS_HOST"),
        "username": os.getenv("REDIS_USERNAME"),
        "password": os.getenv("REDIS_PASSWORD"),
    },
    "STORAGE": {
        "BACKEND": "django_bunny.storage.BunnyStorage",
    },
    "SIZES": {
        "consistent": {
            "PROCESSORS": [
                {"PATH": "nekos_api.processors.gif_resize", "aspect_ratio": "16/9"}
            ]
        }
    },
}

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

X_FRAME_OPTIONS = "SAMEORIGIN"

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
            "builtins": ["django_hosts.templatetags.hosts_override"],
        },
    },
]

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "api.pagination.LimitOffsetPagination",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework_json_api.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework_json_api.parsers.JSONParser",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.SearchFilter",
        "nekos_api.filters.QueryParameterValidation",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "MAX_LIMIT": 50,
    "DEFAULT_LIMIT": 25,
    "SEARCH_PARAM": "filter[search]",
}

JSON_API_FORMAT_FIELD_NAMES = "camelize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_FORMAT_RELATED_LINKS = "dasherize"
JSON_API_UNIFORM_EXCEPTIONS = True

WSGI_APPLICATION = "nekos_api.wsgi.application"
ASGI_APPLICATION = "nekos_api.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv("REDIS_URL")],
        },
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "dj_db_conn_pool.backends.postgresql",
        "NAME": os.getenv("PGDATABASE"),
        "USER": os.getenv("PGUSER"),
        "PASSWORD": os.getenv("PGPASSWORD"),
        "HOST": os.getenv("PGHOST"),
        "PORT": "5432",
        "POOL_OPTIONS": {"POOL_SIZE": 5, "MAX_OVERFLOW": 10, "RECYCLE": 12 * 60 * 60},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
    }
}

STORAGES = {
    "default": {"BACKEND": "django_bunny.storage.BunnyStorage"},
    "staticfiles": {
        "BACKEND": "django_bunny.storage.BunnyStorage",
        "OPTIONS": {"base_dir": "static/", "password": os.getenv("BUNNY_PASSWORD")},
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    "oauth2_provider.backends.OAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
]

oidc_f = open(os.path.join(BASE_DIR, "oidc.key"))
oidc_key = oidc_f.read().strip()
oidc_f.close()

OAUTH2_PROVIDER = {
    "SCOPES": {
        "openid": "OpenID Connect",
        "account:public:retrieve": "Access your public information",
        "account:public:update": "Update your public information",
        "account:email:retrieve": "Access your email address",
        "account:email:update": "Update your email address",
        "account:private:retrieve": "Access your full name",
        "account:private:update": "Update your full name",
        "account:secret-key:retrieve": "Access your secret key",
        "account:secret-key:refresh": "Refresh your secret key",
        "image:create": "Upload images in your name",
        "image:update": "Update images that you have uploaded",
        "image:delete": "Delete images you have uploaded",
        "image:like": "Like images in your name",
        "image:save": "Save images to your library",
        "artist:follow": "Follow artists",
        "category:follow": "Follow categories",
        "character:follow": "Follow characters",
        "list:private": "Access your private image lists",
        "list:create": "Create new image lists in your name",
        "list:update": "Update the image lists that you own",
        "list:delete": "Delete your image lists",
        "user:follow": "Follow users",
        "application:retrieve": "See all the applications you own",
        "application:create": "Create applications in your name",
        "application:update": "Update the applications that you own",
        "application:delete": "Delete the applications you own",
        "webhook:retrieve": "See all the webhooks that you created",
        "webhook:create": "Create webhooks in your name",
        "webhook:update": "Update the webhooks that you own",
        "webhook:delete": "Delete the webhooks that you own",
    },
    "DEFAULT_SCOPES": [
        "account:public:retrieve",
    ],
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": oidc_key,
    "OAUTH2_VALIDATOR_CLASS": "nekos_api.oauth_validators.NekosAPIOAuth2Validator",
    # "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.JSONOAuthLibCore",
    "REFRESH_TOKEN_EXPIRE_SECONDS": timedelta(weeks=4),
    "OIDC_ISS_ENDPOINT": "https://api.nekosapi.com",
}

OAUTH2_PROVIDER_APPLICATION_MODEL = "applications.Application"

CLEAR_EXPIRED_TOKENS_BATCH_SIZE = 100
CLEAR_EXPIRED_TOKENS_BATCH_INTERVAL = 120

AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "https://cdn.nekosapi.com/static/"
STATIC_ROOT = "static/"

MEDIA_URL = "https://cdn.nekosapi.com/"

BUNNY_USERNAME = os.getenv("BUNNY_USERNAME")
BUNNY_PASSWORD = os.getenv("BUNNY_PASSWORD")
BUNNY_REGION = os.getenv("BUNNY_ZONE")
# BUNNY_HOSTNAME = os.getenv("BUNNY_HOSTNAME")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

API_VERSION = "2.4.2"


PROTECTED_API_TOKEN = os.getenv("PROTECTED_API_TOKEN")


if DEBUG:
    LOGIN_URL = f"http://sso.{os.getenv('BASE_DOMAIN')}:8000/login"

    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        f"api.{os.getenv('BASE_DOMAIN')}",
        f"sso.{os.getenv('BASE_DOMAIN')}",
        os.getenv("BASE_DOMAIN"),
    ]
else:
    LOGIN_URL = f"https://sso.{os.getenv('BASE_DOMAIN')}/login"

    ALLOWED_HOSTS = [
        f"api.{os.getenv('BASE_DOMAIN')}",
        f"sso.{os.getenv('BASE_DOMAIN')}",
        f"admin.{os.getenv('BASE_DOMAIN')}",
    ]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        }
    },
}
