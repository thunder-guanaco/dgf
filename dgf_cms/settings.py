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

# See: https://stackoverflow.com/questions/54712982/django-2-0-upgrade-false-positives-on-urls-w001-warning
SILENCED_SYSTEM_CHECKS = ['urls.W001']


def get_env_or_die(env_var):
    value = os.getenv(env_var)
    if not value:
        raise ImproperlyConfigured(f'Missing environment variable \'{env_var}\'')
    return value


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

""""
Rule of thumb:
 * prod: sensible configuration data comes from environment variables
 * dev or test: dummy configuration

"""
ENV = get_env_or_die('DJANGO_ENV')
if ENV not in ['dev', 'test', 'prod']:
    raise ImproperlyConfigured('Environment variable \'DJANGO_ENV\' must be one of {\'dev\', \'test\', \'prod\'}')

if ENV in ['dev', 'test']:
    SECRET_KEY = 'not-really-a-secret'
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
    DATA_DIR = BASE_DIR
    LOG_DIR = BASE_DIR
    LOG_LEVEL = 'INFO'
    DGF_VERSION = 'dev'
    GITHUB_TOKEN = 'nothing'
else:
    SECRET_KEY = get_env_or_die('DJANGO_SECRET_KEY')
    DEBUG = False
    ALLOWED_HOSTS = get_env_or_die('DJANGO_ALLOWED_HOSTS').split(',')
    DATA_DIR = '/home/ubuntu'
    LOG_DIR = os.path.join(DATA_DIR, 'logs')
    LOG_LEVEL = get_env_or_die('DJANGO_LOG_LEVEL')
    DGF_VERSION = get_env_or_die('DJANGO_DGF_VERSION')
    GITHUB_TOKEN = get_env_or_die('DJANGO_GITHUB_TOKEN')

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
            'NAME': get_env_or_die('DJANGO_DB_DATABASE'),
            'USER': get_env_or_die('DJANGO_DB_USER'),
            'PASSWORD': get_env_or_die('DJANGO_DB_PASSWORD'),
        }
    }
    # Django DB Backups
    # https://django-dbbackup.readthedocs.io/en/stable/configuration.html
    DBBACKUP_STORAGE = 'storages.backends.ftp.FTPStorage'
    DBBACKUP_CLEANUP_KEEP = 10
    DBBACKUP_CLEANUP_KEEP_MEDIA = 5
    DBBACKUP_DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
    DBBACKUP_FILENAME_TEMPLATE = 'dgf_db_{datetime}.{extension}'
    DBBACKUP_MEDIA_FILENAME_TEMPLATE = 'dgf_media_{datetime}.{extension}'
    DBBACKUP_STORAGE_OPTIONS = {
        'location': get_env_or_die('DJANGO_FTP_CONNECTION_STRING')
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

# UDisc
UDISC_COURSE_BASE_URL = 'https://udisc.com/courses/{}'
SELENIUM_DRIVER_EXECUTABLE_PATH = os.path.join(BASE_DIR, 'geckodriver')

# PDGA
APPROVED_DISCS_URL = 'https://www.pdga.com/technical-standards/equipment-certification/discs/export'

if ENV == 'test':
    PDGA_BASE_URL = 'http://nowhere.com'
    PDGA_USERNAME = 'nobody'
    PDGA_PASSWORD = 'nothing'
else:
    PDGA_BASE_URL = 'https://api.pdga.com/services/json'
    PDGA_USERNAME = get_env_or_die('DJANGO_PDGA_USERNAME')
    PDGA_PASSWORD = get_env_or_die('DJANGO_PDGA_PASSWORD')

ROOT_URLCONF = 'dgf_cms.urls'
LOGIN_URL = 'login'
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

FILE_UPLOAD_PERMISSIONS = 0o644

# See: https://django-compressor.readthedocs.io/en/stable/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True
COMPRESS_FILTERS = {
    'css': ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.rCSSMinFilter'],
    'js': ['compressor.filters.jsmin.JSMinFilter']
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

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
    'cms.middleware.language.LanguageCookieMiddleware',
    'compression_middleware.middleware.CompressionMiddleware',
]

INSTALLED_APPS = [
    'dgf',
    'django_countries',
    'compressor',
    'dbbackup',

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

LOGIN_REDIRECT_URL = '/'
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
        'fallbacks': ['de'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

CONN_MAX_AGE = 60

LOCALE_PATHS = [
    f'{BASE_DIR}/locale',
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
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'when': 'midnight',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        },
        'dgf': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
