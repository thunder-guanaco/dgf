import os

from django.core.exceptions import ImproperlyConfigured

"""
Django settings for dgf_cms project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

ROOT_INSTALLATION_PATH = '/home/ubuntu'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

""""
Rule of thumb:
 * prod: sensible configuration data comes from environment variables
 * dev or test: dummy configuration

"""
ENV = os.getenv('DJANGO_ENV')
if ENV not in ['dev', 'test', 'prod']:
    raise ImproperlyConfigured('Environment variable \'DJANGO_ENV\' must be one of {\'dev\', \'test\', \'prod\'}')

if ENV in ['dev', 'test']:
    SECRET_KEY = 'not-really-a-secret'
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
    DATA_DIR = os.path.dirname(os.path.dirname(__file__))
else:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    DEBUG = os.getenv('DJANGO_DEBUG')
    ALLOWED_HOSTS = [os.getenv('DJANGO_ALLOWED_HOSTS')]
    DATA_DIR = ROOT_INSTALLATION_PATH

if ENV == 'dev':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'PORT': '3306',
            'NAME': 'dgf_cms',
            'USER': 'dgf',
            'PASSWORD': 'dgf',
        }
    }
elif ENV == 'prod':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'PORT': '3306',
            'NAME': os.getenv('DJANGO_DB_DATABASE'),
            'USER': os.getenv('DJANGO_DB_USER'),
            'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
        }
    }
elif ENV == 'test':
    DATABASES = {
        'default': {
            'CONN_MAX_AGE': 0,
            'ENGINE': 'django.db.backends.sqlite3',
            'HOST': 'localhost',
            'NAME': 'test.db',
            'PASSWORD': '',
            'PORT': '',
            'USER': ''
        }
    }

# PDGA
APPROVED_DISCS_URL = 'https://www.pdga.com/technical-standards/equipment-certification/discs/export'

if ENV == 'test':
    PDGA_BASE_URL = 'http://nowhere.com'
    PDGA_USERNAME = 'nobody'
    PDGA_PASSWORD = 'nothing'
else:
    PDGA_BASE_URL = 'https://api.pdga.com/services/json'
    PDGA_USERNAME = os.getenv('DJANGO_PDGA_USERNAME')
    PDGA_PASSWORD = os.getenv('DJANGO_PDGA_PASSWORD')

ROOT_URLCONF = 'dgf_cms.urls'

WSGI_APPLICATION = 'dgf_cms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'dgf_cms', 'static'),
)
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dgf_cms', 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]

INSTALLED_APPS = [
    'dgf',
    "django_crontab",

    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',
    'djangocms_file',
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'dgf_cms'
]

LOGIN_REDIRECT_URL = '/friends/profile'
LOGOUT_REDIRECT_URL = '/'

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
)

CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': 'English',
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
        {
            'code': 'de',
            'name': 'German',
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
    ],
    'default': {
        'fallbacks': ['en', 'de'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

LOCALE_PATHS = [
    '{}/locale'.format(BASE_DIR),
]

CMS_TEMPLATES = (
    ('fullwidth.html', 'Fullwidth'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} (Thread-{thread:d} - {name}): {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'dgf': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    },
}

CRONJOBS = [
    ('* */6 * * * export DJANGO_ENV=prod; source ~/secrets;', 'dgf.cronjobs.fetch_rating', '>> ~/logs/cronjobs'),
    ('* * */7 * * export DJANGO_ENV=prod; source ~/secrets;', 'dgf.cronjobs.update_approved_discs_cron',
     '>> ~/logs/cronjobs')
]
