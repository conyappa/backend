from .settings import *  # noqa: F401,F403

##################
# AUTHENTICATION #
##################

SIMPLE_JWT.update(  # noqa: F405
    {
        "SIGNING_KEY": "w8/L1-B-Bkov1;cs]mkvh*_6wW&./6m1:p89>.JFtTK$(dF9gn",
        "ALGORITHM": "HS256",
    }
)


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": 5432,
    }
}


#########
# EMAIL #
#########

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_HOST_USER = "example@gmail.com"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


###############
# ENVIRONMENT #
###############

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


###########
# SECRETS #
###########

SECRET_KEY = "m[4xQ]go~21)h6'HWh@Xz4ydn8X]H1vON4E8~`'>zv+cf+rZww"

FINTOC_IS_ENABLED = False
FINTOC_SECRET_KEY = "sk_example_WXUFqk8hMPQ4UA7HafJtZDsPZvabS5af"
FINTOC_LINK_TOKEN = "bsdnsLxwLg4hvIiu_token_MqtIXPNibVqK3XtPBOvmUI1m"
FINTOC_ACCOUNT_ID = "AzrEVH1tFG4z4kTT"
