import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(".env", raise_error_if_not_found=True))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

APPLICATION_NAME = os.getenv("APPLICATION_NAME")

APPLICATION_ALIAS = os.getenv("APPLICATION_ALIAS")

INSTALLED_APPS = [
    "django_q",
    # Default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Installed apps
    "apps.dashboard",
    "apps.accounts",
    "apps.portfolios",
    "apps.stocks",
    "apps.risk_management",
    "apps.live_rates",
]

MIDDLEWARE = [
    "helpers.response.middleware.MaintenanceMiddleware",  # Handles application maintenance mode
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "helpers.context_processors.application",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

CONN_MAX_AGE = 60

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": False,
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

AUTH_USER_MODEL = "accounts.UserAccount"

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
    "apps.accounts.auth_backends.EmailBackend",
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "theme_files"),
    os.path.join(BASE_DIR, "core/static"),
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:signin"

if DEBUG is False:
    # PRODUCTION SETTINGS ONLY
    ALLOWED_HOSTS = ["be.doulab.bloombyte.dev"]

else:
    # DEVELOPMENT SETTINGS ONLY
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "be.doulab.bloombyte.dev"]


CSRF_TRUSTED_ORIGINS = ["https://be.doulab.bloombyte.dev"]

####################
# HELPERS SETTINGS #
####################

HELPERS_SETTINGS = {
    "MAINTENANCE_MODE": {
        "status": os.getenv("MAINTENANCE_MODE", "off").lower() in ["on", "true"],
        "message": os.getenv("MAINTENANCE_MODE_MESSAGE", "default:minimal_dark"),
    },
}

MG_LINK_CLIENT_USERNAME = os.getenv("MG_LINK_CLIENT_USERNAME")
MG_LINK_CLIENT_PASSWORD = os.getenv("MG_LINK_CLIENT_PASSWORD")

Q_CLUSTER = {
    "name": "ekg-global",
    "recycle": 500,
    "compress": True,
    "save_limit": 250,
    "queue_limit": 500,
    "timeout": 30,
    "retry": 60,
    "cpu_affinity": 1,
    "workers": 2,  # Since we are not running any heavy tasks, we can keep this low
    "label": "Django Q",
    "catch_up": False,
    "redis": os.getenv("REDIS_LOCATION"),
    "django_redis": "default",
    "broker": "django_q.brokers.redis_broker.Redis",
}

STOCKS_INDICES_FILE = os.path.join(BASE_DIR, "resources/stocks_indices.csv")
