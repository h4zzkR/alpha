import os
from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'http://217.182.75.251:8000'
DOMAIN = '217.182.75.251:8000' #need for emailing templates
AUTO_CONFIRM = True

SITE_ID = 1
SECRET_KEY = '%vkruwrhxujcdcup=mnk_x1loax+8=4+$@(f2on5l$^hw-yl#_'
DEBUG = True
ALLOWED_HOSTS = ["217.182.75.251", "localhost", "127.0.0.1", "concat.cleverapps.io"]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
    25: 'alert-success',
    20: 'alert-info',
    10: 'alert-info',
    30: 'alert-warning',
    40: 'alert-danger'
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
MESSAGE_LEVEL = 25

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'apps.project.apps.ProjectConfig',
    'apps.user.apps.UserConfig',
    'apps.events.apps.EventsConfig',
    'apps.main.apps.MainConfig',
    'taggit',
    'django.contrib.sites',

    'social_django',  # <--
]

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <--
]

ROOT_URLCONF = 'alpha.urls'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                "django.template.context_processors.static",

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',  # <--
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.template.context_processors.request",
    'django.contrib.messages.context_processors.messages',
    "django.template.context_processors.media",
    "django.template.context_processors.static",
)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GITHUB_KEY = 'e87f58fb9971ac0bd0ae'
SOCIAL_AUTH_GITHUB_SECRET = 'a57439a004cf205d0f131102ddb7a636fdb0f7b7'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'apps.user.views.save_profile',
)

LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
LOGIN_REDIRECT_URL = '/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'bhq17eglljztxpcwh9k1',

        'USER': 'uen2a9h3qu5akdyavlua',

        'PASSWORD': 'z6e2Gc6z6c86vG9Dh6AD',

        'HOST': 'bhq17eglljztxpcwh9k1-postgresql.services.clever-cloud.com',

        'PORT': '5432',



    }

}
# DATABASES = {
#
#     'default': {
#
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#
#         'NAME': 'concat',
#
#         'USER': 'concat',
#
#         'PASSWORD': 's1XTPKlOjWo4',
#
#         'HOST': 'localhost',
#
#         'PORT': '5432',
#
#
#
#     }
#
# }

USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive users for before
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7

WSGI_APPLICATION = 'alpha.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'concat.no.reply@gmail.com'
EMAIL_HOST_PASSWORD = 'b&FS!(h@<4}sF`Ss'

if not DEBUG:
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

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/722
# SECURE_SSL_REDIRECT = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'templates/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
