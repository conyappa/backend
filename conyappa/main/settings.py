import datetime as dt
import os
import sys

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

int_bool = lambda x: bool(int(x))


##########################
# APPLICATION DEFINITION #
##########################

THIRD_PARTY = [
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "django_extensions",
    "admin_numeric_filter",
    "rest_framework_simplejwt.token_blacklist",
]

FIRST_PARTY = [
    "accounts.apps.AccountsConfig",
    "banking.apps.BankingConfig",
    "docs.apps.DocsConfig",
    "lottery.apps.LotteryConfig",
    "scheduler.apps.SchedulerConfig",
]

BUILT_IN = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

INSTALLED_APPS = THIRD_PARTY + FIRST_PARTY + BUILT_IN


##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = "accounts.User"

ACCESS_TOKEN_LIFETIME_MINUTES = int(os.environ.get("ACCESS_TOKEN_LIFETIME_MINUTES", "15"))
REFRESH_TOKEN_LIFETIME_HOURS = int(os.environ.get("REFRESH_TOKEN_LIFETIME_HOURS", "336"))

# LEGACY
SLIDING_TOKEN_LIFETIME_DAYS = int(os.environ.get("SLIDING_TOKEN_LIFETIME_DAYS", "365"))

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": dt.timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": dt.timedelta(hours=REFRESH_TOKEN_LIFETIME_HOURS),
    "SIGNING_KEY": os.environ.get("JWT_SIGNING_KEY"),
    "ALGORITHM": os.environ.get("JWT_ALGORITHM"),
    "ROTATE_REFRESH_TOKENS": True,
    # LEGACY
    "AUTH_TOKEN_CLASSES": [
        "rest_framework_simplejwt.tokens.AccessToken",
        "rest_framework_simplejwt.tokens.SlidingToken",
    ],
    "SLIDING_TOKEN_LIFETIME": dt.timedelta(days=SLIDING_TOKEN_LIFETIME_DAYS),
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
EMAIL_USE_TLS = int_bool(os.environ.get("EMAIL_USE_TLS", "0"))
EMAIL_USE_SSL = int_bool(os.environ.get("EMAIL_USE_SSL", "0"))
EMAIL_USE_LOCALTIME = True


###############
# ENVIRONMENT #
###############

TEST = "test" in sys.argv
DJANGO_ENV = os.environ.get("DJANGO_ENV")
DEBUG = DJANGO_ENV == "development"
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
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "level": "CRITICAL",
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

TICKET_COST = int(os.environ.get("TICKET_COST", "5000"))
INITIAL_EXTRA_TICKETS_TTL = list(map(int, os.environ.get("INITIAL_EXTRA_TICKETS_TTL", "1").split(" ")))
PICK_RANGE = tuple(range(int(os.environ.get("MIN_PICK", "1")), int(os.environ.get("MAX_PICK", "30")) + 1))
PRIZES = tuple(map(int, os.environ.get("PRIZES", "0 0 0 0 0 0 0 0").split(" ")))
IS_SHARED_PRIZE = tuple(map(int_bool, os.environ.get("IS_SHARED_PRIZE", "0 0 0 0 0 0 0 0").split(" ")))


##################
# REST FRAMEWORK #
##################

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
}


###########
# SECRETS #
###########

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY")

FINTOC_IS_ENABLED = int_bool(os.environ.get("FINTOC_IS_ENABLED", "0"))
FINTOC_SECRET_KEY = os.environ.get("FINTOC_SECRET_KEY")
FINTOC_LINK_TOKEN = os.environ.get("FINTOC_LINK_TOKEN")
FINTOC_ACCOUNT_ID = os.environ.get("FINTOC_ACCOUNT_ID")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_PARTITION = "aws"
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")

AWS_CHOOSE_RESULT_LAMBDA = os.environ.get("AWS_CHOOSE_RESULT_LAMBDA")
AWS_CREATE_DRAW_LAMBDA = os.environ.get("AWS_CREATE_DRAW_LAMBDA")
AWS_FETCH_MOVEMENTS_LAMBDA = os.environ.get("AWS_FETCH_MOVEMENTS_LAMBDA")
AWS_RANDOM_SEED_LAMBDA = os.environ.get("AWS_RANDOM_SEED_LAMBDA")


##########
# SENTRY #
##########

sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN", ""), integrations=[DjangoIntegration()], environment=DJANGO_ENV)


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
