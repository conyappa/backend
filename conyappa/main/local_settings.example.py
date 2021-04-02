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

HOME = "192.168.xxx.yyy"
PLATANUS = "192.168.xxx.yyy"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", HOME, PLATANUS]


##############
# PARAMETERS #
##############

MAX_TICKETS = float("inf")


###########
# SECRETS #
###########

SECRET_KEY = "m[4xQ]go~21)h6'HWh@Xz4ydn8X]H1vON4E8~`'>zv+cf+rZww"
INTERNAL_KEY = "XSi,7l|7.hC*w-4z[P+.&82:v]vgCGN3_XG<8tu`!|i/89<^x;"

FINTOC_IS_ENABLED = False
FINTOC_SECRET_KEY = "sk_example_WXUFqk8hMPQ4UA7HafJtZDsPZvabS5af"
FINTOC_LINK_TOKEN = "bsdnsLxwLg4hvIiu_token_MqtIXPNibVqK3XtPBOvmUI1m"
FINTOC_ACCOUNT_ID = "AzrEVH1tFG4z4kTT"

AWS_ACCESS_KEY_ID = "AKIA4AWHNDASTGTJVSZA"
AWS_SECRET_ACCESS_KEY = "KnZB+StfliRAvr7TX283URDgprv0gZ+IHx8x6JW2"

AWS_REGION_NAME = "example-region"
AWS_ACCOUNT_ID = "0123456789"

AWS_CREATE_DRAW_LAMBDA = "conyappa-stage-functionName"
AWS_RANDOM_SEED_LAMBDA = "conyappa-stage-functionName"
