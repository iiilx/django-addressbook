DEBUG = True
DEBUG_TEMPLATE = True
SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/django-addressbook-devel.db'
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'south',
    'crispy_forms',
    'addressbook',
    'django_nose',
]

ROOT_URLCONF = 'addressbook.testurls'
SECRET_KEY = 'test-secret-key'
STATIC_URL = '/static/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
