"""
Django settings for ib_gamification_backend project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development conf - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

ROOT_URLCONF = 'tdd_practice.urls'

CSRF_COOKIE_SECURE = False

WSGI_APPLICATION = 'tdd_practice.wsgi.application'

SCRIPT_NAME = "/" + os.environ.get("STAGE", "alpha")

################## CORS #####################

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1',
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'x-api-key',
    'x-source'
)
#*************** Internationalization *******************#
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

RAVEN_CONFIG = {
    'dsn': os.environ.get("RAVEN_DSN"),
    'release': os.environ.get('STAGE')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'handlers': {
         'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            "filters": ["request_id"],
        },
        'logentries_handler': {
            'level': 'DEBUG',
            'formatter': 'console',
            'token': os.environ.get('LOGENTRIES_TOKEN', '36f1615d-7012-4150-97c6-a0e08c8cae03'),
            'class': 'logentries.LogentriesHandler',
            "filters": ["request_id"],
        },
    },
    'formatters': {
        'console': {
            'format': "[%(request_id)s] [ib_gamification_backend - "+os.environ.get("STAGE", "local")+
                      '] %(levelname)-8s [%(asctime)s]  '
                      '[%(pathname)s] [%(filename)s]'
                      '[%(funcName)s] [%(lineno)d]: %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
        'dsu.debug': {
            'handlers': ['logentries_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'logentries': {
            'handlers': ['console', 'logentries_handler'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}
# ********************** Installed Apps ****************************

INSTALLED_APPS = [
    'django.contrib.admin',  # admin interface
    'django.contrib.auth',  # django authentication
    'django.contrib.contenttypes',  # response content types used in admin
    'django.contrib.sessions',  # django sessions used in admin
    'django.contrib.messages',  # info, success, error message in response. admin requires this
    'django.contrib.staticfiles',  # host the static files
]

THIRD_PARTY_APPS_BASE = [
    # oauth
    'oauth',
    'oauth2_provider',
    # aws storage
    'storages',
    # django rest framework
    'rest_framework',
    'rest_framework_xml',  # xml renderers, parsers
    'corsheaders',

    # raven
    'raven.contrib.django.raven_compat',

    # CUSTOM APPS
    'django_swagger_utils',

    # django fine uploader
    'django_fine_uploader_s3',
    'cacheops',
]
INSTALLED_APPS += THIRD_PARTY_APPS_BASE

# ********************** Password Validators ***************************
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# ************************* Django Rest Framework ******************************
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework.renderers.AdminRenderer',
    ),
    'EXCEPTION_HANDLER': 'django_swagger_utils.drf_server.exceptions.drf_custom_exception.custom_exception_handler'
}

# ************************** Templates ******************************
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


# *********************** Middleware *************************#

MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',  # request logging
    'django.contrib.sessions.middleware.SessionMiddleware',  # django sessions, usefull in admin
    'corsheaders.middleware.CorsMiddleware',  # cors headers middleware
    'django.middleware.common.CommonMiddleware',
    # handling the url redirect, adding / in the end of url.
    # ref https://docs.djangoproject.com/en/1.9/ref/middleware/#django.middleware.common.CommonMiddleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # set request.user value after authenticating
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # used in session invalidation, admin requires this
    'django.contrib.messages.middleware.MessageMiddleware',
    # messaging framework middleware, django admin requires this
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # save from clickjack attack ref https://docs.djangoproject.com/en/1.9/ref/clickjacking/
    'django.middleware.locale.LocaleMiddleware',
]

# TEST_RUNNER = 'snapshottest.django.TestRunner'

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('te', _('Telugu')),
    ('hi', _('Hindi')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': os.environ.get("FCM_SERVER_KEY", "")
}

REDIS_HOST = os.environ.get("REDIS_PORT_6379_TCP_ADDR", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_LEADERBOARD_DB = os.environ.get("REDIS_LEADERBOARD_DB", 2)

# <GROUP>
IB_GROUP_REQUEST_TYPE = os.environ.get("IB_GROUPS_REQUEST_TYPE", "LIBRARY")
# </GROUP>

# <LEADERBOARD>
IB_LEADERBOARDS_REQUEST_TYPE = os.environ.get("IB_LEADERBOARDS_REQUEST_TYPE", "LIBRARY")
# </LEADERBOARD>

# <ACTION>
IB_ACTION_REQUEST_TYPE = os.environ.get("IB_ACTION_REQUEST_TYPE", "LIBRARY")
# </ACTION>

# <SOCIAL>
IB_SOCIAL_REQUEST_TYPE = os.environ.get("IB_SOCIAL_REQUEST_TYPE", "LIBRARY")
# </SOCIAL>

# <NOTIFICATIONS>
IB_NOTIFICATIONS_REQUEST_TYPE = os.environ.get("IB_NOTIFICATIONS_REQUEST_TYPE", "LIBRARY")
# </NOTIFICATIONS>

IB_RESOURCE_REQUEST_TYPE = os.environ.get("IB_RESOURCE_REQUEST_TYPE", "LIBRARY")

# <CHAT>
IB_CHAT_REQUEST_TYPE = 'SERVICE'
IB_CHAT_BASE_URL = 'https://ibc-chat-backend-alpha.apigateway.in/'

IBC_CHAT_REQUEST_TYPE = 'SERVICE'
IBC_CHAT_BASE_URL = 'https://ibc-chat-backend-alpha.apigateway.in/'

CHAT_SESSION_BASE_URL = 'https://ibc-chat-backend-alpha.apigateway.in/'
CHAT_SESSION_REQUEST_TYPE='SERVICE'
IB_CHAT_APP_ID = ''
IB_CHAT_ACCESS_TOKEN = ''
# </CHAT>

# <IB_ADS_CAMPAIGN>
IB_ADS_CAMPAIGN_REQUEST_TYPE = 'SERVICE'
IB_ADS_CAMPAIGN_BASE_URL = 'https://ibc-ads-backend-alpha.apigateway.in'
IB_ADS_CAMPAIGN_SOURCE = os.environ.get("SOURCE", "IB_ADS")
IB_ADS_CAMPAIGN_APP_ACCESS_TOKEN = os.environ.get('IB_ADS_CAMPAIGN_APP_ACCESS_TOKEN', '')
# </IB_ADS_CAMPAIGN>

# sms & email
import base64
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = str(os.environ.get("EMAIL_HOST", ""))
EMAIL_PORT = str(os.environ.get("EMAIL_PORT", ""))
EMAIL_HOST_USER = str(os.environ.get("EMAIL_HOST_USER", ""))
EMAIL_HOST_PASSWORD = base64.b64decode(os.environ.get("EMAIL_HOST_PASSWORD", ""))
EMAIL_USE_TLS = str(os.environ.get("EMAIL_USE_TLS", ""))
DEFAULT_SENDER_EMAIL = str(os.environ.get("DEFAULT_SENDER_EMAIL", ""))

STAGE = os.environ.get("STAGE", "local")
SOURCE = "AR_VR"

LOGGER_NAME = "logentries"

ENABLE_REAL_TIME = False

# ****************** App Source Config ******************
GAS_AUTH_BACKEND_SOURCE = "gas-auth-backend-source"
SOCIAL_ID_SALT = "0j4XvkQHARXAgpOZGOUxGcRsEkZ52Tz9"

# ****************** COGNITO ******************************
COGNITO_POOL_REGION_NAME = os.environ.get("COGNITO_POOL_REGION_NAME",
                                          "ap-south-1")
COGNITO_POOL_ID = os.environ.get("COGNITO_POOL_ID", "ap-south-1_XXXXXXX")
COGNITO_POOL_CLIENT_ID = os.environ.get("COGNITO_POOL_CLIENT_ID",
                                        "")
COGNITO_POOL_CLIENT_SECRET = os.environ.get("COGNITO_POOL_CLIENT_SECRET",
                                            "")
COGNITO_POOL_CLIENT_REDIRECT_URI = os.environ.get(
    "COGNITO_POOL_CLIENT_REDIRECT_URI",
    "")
COGNITO_POOL_CLIENT_IDP_DOMAIN_URL = os.environ.get(
    "COGNITO_POOL_CLIENT_IDP_DOMAIN_URL",
    "")
COGNITO_MAX_PHONE_NUMBER_CHANGES = int(
    os.environ.get("COGNITO_MAX_PHONE_NUMBER_CHANGES", "2"))
COGNITO_IDENTITY_POOL_ID = os.environ.get("COGNITO_IDENTITY_POOL_ID",
                                          "")
COGNITO_ENCRYPTION_KEY = os.environ.get("COGNITO_ENCRYPTION_KEY", "local_key")

# ******************** OTP - Message91 **********************
MAX_OTPS_COUNT = int(os.environ.get('MAX_OTPS_COUNT', "3"))
OTP_EXPIRE_MINUTES = int(os.environ.get('OTP_EXPIRE_MINUTES', "15"))
SMS_PROVIDER = os.environ.get("SMS_PROVIDER", "MSG91")
SNS_REGION_NAME = os.environ.get("SNS_REGION_NAME", "us-east-1")

MSG91_AUTH_KEY = os.environ.get("MSG91_AUTH_KEY", "")
MSG91_DEFAULT_SENDER_ID = os.environ.get("MSG91_DEFAULT_SENDER_ID", "GAS_AUTH")
DEFAULT_MSG91_RESEND_OPTION = os.environ.get("DEFAULT_MSG91_RESEND_OPTION",
                                             "voice")

# ******************** AWS Configuration *********************
AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID", "")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "ap-south-1")
MEDIAFILES_LOCATION = os.environ.get("MEDIAFILES_LOCATION", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_CLOUDFRONT_DOMAIN = os.environ.get("AWS_CLOUDFRONT_DOMAIN", "")

WHITELISTED_PHONE_NUMBERS = str(
    os.environ.get("WHITELISTED_PHONE_NUMBERS", "+918437479642"))

FOO_USER_TO_HEADERS_CONVERTER = 'tdd_practice.common.foo_user_to_headers_converter.foo_user_to_headers_converter'

CREATE_USER_ON_API_KEY_HEADER = True

CACHEOPS_REDIS = {
    'host': os.environ.get('CACHEOPS_REDIS_HOST', '127.0.0.1'),
    'port': os.environ.get('CACHEOPS_REDIS_PORT', 6379),
    'db': os.environ.get('CACHEOPS_REDIS_DB', 0),
    'socket_timeout': 3,
}

CACHEOPS_DEGRADE_ON_FAILURE = True

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60
}

CACHEOPS = {
}

CUSTOM_SCOPES_CHECK_FUNCTION = 'gas_auth_backend.common.check_custom_scopes.check_custom_scopes'

PRINT_LOCK_LOGS = os.environ.get('PRINT_LOCK_LOGS', True)

# Stage config set in L:313
AWS_KEY_STORE_S3_REGION_NAME = os.environ.get(
    'AWS_KEY_STORE_S3_REGION_NAME', 'ap-south-1'
)
AWS_KEY_STORAGE_BUCKET_NAME = os.environ.get(
    'AWS_KEY_STORAGE_BUCKET_NAME',
    'keystore-s3-bucket'
)
# from redisco import connection_setup
# connection_setup(
#     host=os.environ.get('KEY_STORE_REDIS_HOST', REDIS_HOST),
#     port=os.environ.get('KEY_STORE_REDIS_PORT', REDIS_PORT),
#     db=os.environ.get('KEY_STORE_REDIS_DB', 4)
# )
KEY_STORE_VALUE_MAX_LENGTH = 50000
STORE_CONFIG = {
    'KeyStore': {
        'NAMESPACE': os.environ.get('KEY_STORE_NAMESPACE', 'gas'),
        'VALUE_MAX_LENGTH': max(
            int(os.environ.get(
                'KEY_STORE_VALUE_MAX_LENGTH', KEY_STORE_VALUE_MAX_LENGTH))
            , KEY_STORE_VALUE_MAX_LENGTH
        )
    }
}
