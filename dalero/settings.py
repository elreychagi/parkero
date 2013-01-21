# Django settings for dalero project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dalero_db',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Caracas'

LANGUAGE_CODE = 'es-la'

SITE_ID = 1

USE_I18N = False

USE_L10N = False

USE_TZ = True

MEDIA_ROOT = os.path.join(ROOT_PATH, '../media/')

MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(ROOT_PATH, '../static/')

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'w&amp;0hk4q0=op_h!l)_o1@efd^dyqf(%(dgut^)gl#)7qa#g4ad'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'dalero.urls'

WSGI_APPLICATION = 'dalero.wsgi.application'

TEMPLATE_DIRS = (os.path.join(ROOT_PATH, '../templates/'),)

LOGIN_URL = '/login/'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'website',
    'usuarios',
    'geo',
    'comentarios'
)

TWITTER = {'KEY' : 'QtDrXHh2rKOzAdbtt9WGIg',
           'SECRET' : 'mIJlwd8UlUCD2jIMBr00mEaNVJc6Xfwg2qfOeKLP6A',
           'CALLBACK' : 'http://dalero.net/users/twitter_callback/'}

FACEBOOK = {'KEY' : '437709029599876',
            'SECRET' : 'aae3a045a95c8296770d37001b027ee9',
            'CALLBACK' : 'http://dalero.net/users/facebook_callback/'}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}