import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from dgf_cms.views import csrf_failure

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

"""
Rule of thumb:
 * prod: sensible configuration data comes from environment variables
 * dev or test: dummy configuration

"""
ENV = get_env_or_die('DJANGO_ENV')
if ENV not in ['dev', 'test', 'prod']:
    raise ImproperlyConfigured('Environment variable \'DJANGO_ENV\' must be one of {\'dev\', \'test\', \'prod\'}')

if ENV == 'dev':
    # Add debug variables when rendering pages from localhost (while developing)
    # https://docs.djangoproject.com/en/4.0/ref/settings/#internal-ips
    INTERNAL_IPS = (
        '127.0.0.1',
    )

if ENV in ['dev', 'test']:
    SECRET_KEY = 'not-really-a-secret'
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver'] + [f'192.168.0.{n}' for n in range(0, 256)]
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

CORS_ALLOWED_ORIGINS = [
    'https://discgolfmetrix.com',
]
CORS_ALLOW_METHODS = [
    "GET",
]

CSRF_FAILURE_VIEW = csrf_failure


# Django DB and media Backups
# https://django-dbbackup.readthedocs.io/en/stable/configuration.html
def dbbackup_cleanup_filter(filename):
    return '-01_' in filename


if ENV == 'prod':
    DBBACKUP_STORAGE = 'storages.backends.ftp.FTPStorage'
    DBBACKUP_STORAGE_OPTIONS = {
        'location': get_env_or_die('DJANGO_FTP_CONNECTION_STRING')
    }
    DBBACKUP_DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
    DBBACKUP_CLEANUP_FILTER = dbbackup_cleanup_filter
    DBBACKUP_FILENAME_TEMPLATE = 'dgf_db_{datetime}.{extension}'
    DBBACKUP_MEDIA_FILENAME_TEMPLATE = 'dgf_media_{datetime}.{extension}'
    DBBACKUP_CLEANUP_KEEP = 30
    DBBACKUP_CLEANUP_KEEP_MEDIA = 15

# UDisc
UDISC_COURSE_BASE_URL = 'https://udisc.com/courses/{}'
SELENIUM_DRIVER_EXECUTABLE_PATH = os.path.join(BASE_DIR, 'geckodriver')

# PDGA
PDGA_PAGE_BASE_URL = 'https://www.pdga.com'
PDGA_EVENT_URL = PDGA_PAGE_BASE_URL + '/tour/event/{}'
PDGA_DATE_FORMAT = '%Y-%m-%d'
APPROVED_DISCS_URL = 'https://www.pdga.com/technical-standards/equipment-certification/discs/export'
PDGA_BASE_URL = 'https://api.pdga.com/services/json'

if ENV == 'test':
    PDGA_USERNAME = 'nobody'
    PDGA_PASSWORD = 'nothing'
else:
    PDGA_USERNAME = get_env_or_die('DJANGO_PDGA_USERNAME')
    PDGA_PASSWORD = get_env_or_die('DJANGO_PDGA_PASSWORD')

# GERMAN TOUR
GT_DATE_FORMAT = '%d.%m.%Y'
GT_RATING_PAGE = 'https://rating.discgolf.de/detail.php?gtn={}'
GT_LIST_PAGE = 'https://turniere.discgolf.de/index.php?p=events'
GT_RESULT_LIST_PAGE = 'https://turniere.discgolf.de/index.php?p=events&sp=list-results-overview'
GT_DETAILS_PAGE = 'https://turniere.discgolf.de/index.php?p=events&sp=view&id={}'
GT_ATTENDANCE_PAGE = 'https://turniere.discgolf.de/index.php?p=events&sp=list-players&id={}'
GT_RESULTS_PAGE = 'https://turniere.discgolf.de/index.php?p=events&sp=list-results&id={}'

# DISC GOLF METRIX
DISC_GOLF_METRIX_COMPETITION_ENDPOINT = 'https://discgolfmetrix.com/api.php?content=result&id={}'
DISC_GOLF_METRIX_TOURNAMENT_PAGE = 'https://discgolfmetrix.com/{}'
DISC_GOLF_METRIX_DATE_FORMAT = '%Y-%m-%d'

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

if ENV == 'prod':
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

REVIEWER_GROUP = 'Reviewer'
BACKGROUND_FOLDER = 'Hintergrund'

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
    'corsheaders.middleware.CorsMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.security.SecurityMiddleware',
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
    'django_user_agents.middleware.UserAgentMiddleware',
]

INSTALLED_APPS = [
    'dgf',
    'dgf_league',
    'dgf_images',
    'dgf_cookies',
    'django_countries',
    'compressor',
    'dbbackup',
    'django_user_agents',
    'mathfilters',
    'cookie_consent',
    'django_light',
    'jazzmin',
    'corsheaders',

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
    'django_admin_listfilter_dropdown',
    'djangocms_text_ckeditor',
    'djangocms_file',
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
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

    'djangocms_frontend',
    'djangocms_frontend.contrib.accordion',
    'djangocms_frontend.contrib.alert',
    'djangocms_frontend.contrib.badge',
    'djangocms_frontend.contrib.card',
    'djangocms_frontend.contrib.carousel',
    'djangocms_frontend.contrib.collapse',
    'djangocms_frontend.contrib.content',
    'djangocms_frontend.contrib.grid',
    'djangocms_frontend.contrib.icon',
    'djangocms_frontend.contrib.image',
    'djangocms_frontend.contrib.jumbotron',
    'djangocms_frontend.contrib.link',
    'djangocms_frontend.contrib.listgroup',
    'djangocms_frontend.contrib.media',
    'djangocms_frontend.contrib.tabs',
    'djangocms_frontend.contrib.utilities',

    'dgf_cms',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

USE_TZ = True

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = 'de'
DEFAULT_TRANSLATION_LANGUAGE = 'en'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

# IMPORTANT: German should be the first one ALWAYS
# https://docs.django-cms.org/en/latest/reference/configuration.html#std-setting-CMS_LANGUAGES
CMS_LANGUAGES = {
    1: [
        {
            'code': 'de',
            'name': _('German'),
            'public': True,
            'hide_untranslated': False,
            'redirect_on_fallback': False,
        },
        {
            'code': 'en',
            'name': _('English'),
            'public': True,
            'hide_untranslated': False,
            'redirect_on_fallback': False,
        },
    ],
    'default': {
        'fallbacks': ['de', 'en'],
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': False,
    },
}

CONN_MAX_AGE = 60

LOCALE_PATHS = [
    f'{BASE_DIR}/locale',
]

CMS_TEMPLATES = (
    ('fullwidth.html', 'Fullwidth'),
    ('static_placeholders.html', 'Static Placeholders (ONLY FOR ADMINS)'),
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

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Django 3.0 changed the default behaviour of the XFrameOptionsMiddleware from SAMEORIGIN to DENY.
# In order for django CMS to function, X_FRAME_OPTIONS needs to be set to SAMEORIGIN
# https://docs.django-cms.org/en/latest/upgrade/3.7.2.html
X_FRAME_OPTIONS = 'SAMEORIGIN'

COOKIE_CONSENT_NAME = 'cookie_consent'

# Docs: https://django-jazzmin.readthedocs.io/configuration/
JAZZMIN_SETTINGS = {

    'site_brand': 'Disc Golf Friends',
    'site_logo': '/img/logo.png',
    'site_logo_classes': 'elevation-0',
    'welcome_sign': 'Disc Golf Friends Admin',
    'copyright': 'Disc Golf Friends Dortmund e.V',
    'search_model': 'dgf.Friend',
    'show_sidebar': True,
    'navigation_expanded': False,
    'order_with_respect_to': ['dgf', 'dgf.friend', 'dgf.tournament', 'dgf.bagtagchange',
                              'dgf_images', 'dgf_images.imagegenerator',
                              'dgf_league', 'dgf_league.team', 'dgf_league.match', 'dgf_league.friendwithoutteam',
                              'auth',
                              'cms'],

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    'icons': {
        'dgf': 'fas fa-users',
        'dgf.friend': 'fas fa-user',
        'dgf.tournament': 'fas fa-medal',
        'dgf.bagtagchange': 'fas fa-tag',
        'dgf.course': 'fas fa-tree',
        'dgf.githubissue': 'fas fa-newspaper',
        'dgf.tour': 'fas fa-route',
        'dgf_images': 'fas fa-images',
        'dgf_images.imagegenerator': 'fas fa-print',
        'dgf_league': 'fas fa-medal',
        'dgf_league.team': 'fas fa-users',
        'dgf_league.match': 'fas fa-table',
        'dgf_league.friendwithoutteam': 'fas fa-users',
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.group': 'fas fa-users',
    },

    # this should stay to false because otherwise it messes up with JS code from DjangoCMS
    'related_modal_active': False,

    # Relative paths to custom CSS/JS scripts (must be present in static files)
    'custom_css': 'css/admin.css',
    'custom_js': None,

    'show_ui_builder': True,
    'changeform_format': 'horizontal_tabs',
}

JAZZMIN_UI_TWEAKS = {
    'accent': 'accent-navy',
    'navbar': 'navbar-navy navbar-dark',
    'navbar_fixed': True,
    'sidebar': 'sidebar-light-navy',
    'sidebar_nav_child_indent': True,
    'sidebar_nav_flat_style': True,
    'theme': 'default',
    'dark_mode_theme': None,
    'button_classes': {
        'primary': 'btn-outline-primary',
        'secondary': 'btn-outline-secondary',
        'info': 'btn-outline-info',
        'warning': 'btn-outline-warning',
        'danger': 'btn-outline-danger',
        'success': 'btn-outline-success'
    },
}
