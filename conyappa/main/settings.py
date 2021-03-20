import datetime as dt
import os
import sys

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


##########################
# APPLICATION DEFINITION #
##########################

INSTALLED_APPS = [
    # Third party apps.
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "django_extensions",
    "admin_numeric_filter",
    # First party apps.
    "accounts.apps.AccountsConfig",
    "banking.apps.BankingConfig",
    "docs.apps.DocsConfig",
    "lottery.apps.LotteryConfig",
    # Built-in apps.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]


##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = "accounts.User"

SLIDING_TOKEN_LIFETIME = os.environ.get("SLIDING_TOKEN_LIFETIME", 365)

SIMPLE_JWT = {
    "SLIDING_TOKEN_LIFETIME": dt.timedelta(days=SLIDING_TOKEN_LIFETIME),
    "SIGNING_KEY": os.environ.get("JWT_SIGNING_KEY"),
    "ALGORITHM": os.environ.get("JWT_ALGORITHM"),
    "AUTH_TOKEN_CLASSES": ["rest_framework_simplejwt.tokens.SlidingToken"],
}


#####################
# COMMON MIDDLEWARE #
#####################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


########
# CORS #
########

CORS_ORIGIN_ALLOW_ALL = True


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(ssl_require=True)


#########
# EMAIL #
#########

ADMINS = [("Ariel Martínez", "ariel@conyappa.cl")]
MANAGERS = [("Ariel Martínez", "ariel@conyappa.cl")]
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_PORT = int(os.environ.get("EMAIL_HOST_PORT", "25"))
EMAIL_USE_TLS = bool(int(os.environ.get("EMAIL_USE_TLS", "0")))
EMAIL_USE_SSL = bool(int(os.environ.get("EMAIL_USE_SSL", "0")))
EMAIL_USE_LOCALTIME = True


###############
# ENVIRONMENT #
###############

TEST = "test" in sys.argv
DEBUG = os.environ.get("DJANGO_ENV") == "development"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")


##################
# HTML TEMPLATES #
##################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "main", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


###########
# LOGGING #
###########

PROPAGATE_EXCEPTIONS = True
DEFAULT_LOGGING_LEVEL = "INFO" if DEBUG else "WARNING"
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", DEFAULT_LOGGING_LEVEL)
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
        "level": LOGGING_LEVEL,
    },
}


##############
# PARAMETERS #
##############

MAX_TICKETS = int(os.environ.get("MAX_TICKETS", "4"))
TICKET_COST = int(os.environ.get("TICKET_COST", "5000"))
INITIAL_EXTRA_TICKETS_TTL = list(map(int, os.environ.get("INITIAL_EXTRA_TICKETS_TTL", "1").split(" ")))
PICK_RANGE = tuple(range(int(os.environ.get("MIN_PICK", "1")), int(os.environ.get("MAX_PICK", "30")) + 1))
PRIZES = tuple(map(int, os.environ.get("PRIZES", "10 20 50 100 200 500 1000 5000").split(" ")))
BANK_ACCOUNT = os.environ.get("BANK_ACCOUNT")


##################
# REST FRAMEWORK #
##################

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


###########
# SECRETS #
###########

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY")

FINTOC_IS_ENABLED = bool(int(os.environ.get("FINTOC_IS_ENABLED", "0")))
FINTOC_SECRET_KEY = os.environ.get("FINTOC_SECRET_KEY")
FINTOC_LINK_TOKEN = os.environ.get("FINTOC_LINK_TOKEN")
FINTOC_ACCOUNT_ID = os.environ.get("FINTOC_ACCOUNT_ID")


##########
# SENTRY #
##########

sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN", ""), integrations=[DjangoIntegration()])


################
# STATIC FILES #
################

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


########
# URLS #
########

ROOT_URLCONF = "main.urls"
APPEND_SLASH = False


########
# WSGI #
########

WSGI_APPLICATION = "main.wsgi.application"
