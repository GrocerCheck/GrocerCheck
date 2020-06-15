"""
Django settings for grocercheck project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from os.path import expanduser
import json
from celery.schedules import crontab


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

#SECRET_KEY = '$*7$lu*br%(vzw%o$d289!5236)6%5(lz_3s((36-9=4^8w$@p'

try:
    SECRET_KEY = open("/home/bitnami/keys/djangokey.txt").readline()
except:
    SECRET_KEY = open(expanduser("~")+"/keys/djangokey.txt").readline()


try:
    servername = open("/home/bitnami/keys/servername.txt").readline()
except:
    try:
        servername = open(expanduser("~")+"/keys/servername.txt").readline()

    except:
        print("ERROR: SERVERNAME NOT FOUND")
        servername = ''
        CELERY_BEAT_SCHEDULE = {}




# SECURITY WARNING: don't run with debug turned on in production

if (("dev" in servername) or ("DEV" in servername)):
    DEBUG = True

elif ("bitnami" in BASE_DIR):
    DEBUG = False

else:
    DEBUG = False

ALLOWED_HOSTS = ['www.grocercheck.ca', 'dev.grocercheck.ca', 'grocercheck.ca',
                 '52.13.81.19', '44.230.40.10', '52.10.195.42',  '54.188.229.231',
                 '172.26.13.17', '127.0.0.1', '172.26.0.205', '172.26.28.120',
                 '172.26.11.143', '172.26.1.22', '172.26.10.238', '172.26.3.142']

#Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'map.apps.MapConfig',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'grocercheck.urls'

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

WSGI_APPLICATION = 'grocercheck.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db1.sqlite3'),
    }
}


ADMINS = (
    ('Brian Chen', 'brian@grocercheck.ca'),
    ('Andy Liang', 'andy@grocercheck.ca'),
)

MANAGERS = (
    ('Brian Chen', 'brian@grocercheck.ca'),
    ('Andy Liang', 'andy@grocercheck.ca'),
)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/map/static/'

try:
    MEDIA_ROOT = '/opt/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/map/media/'
    STATIC_ROOT = '/opt/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/map/static/'
except:
#these dirs might not be exactly where we want them but we aren't using them much atm
    MEDIA_ROOT = os.path.dirname(os.getcwd()) + "/map/media/"
    STATIC_ROOT = os.path.dirname(os.getcwd()) + "/map/static/"

#--------------------------------PROXY------------------------------
try:
    p = json.load(open("/home/bitnami/keys/luminati.txt"))
except:
    p = {}
#----------------------------------CELERY----------------------------------------------

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Vancouver'

try:
    pg_creds = json.load(open("/home/bitnami/keys/postgreDB.json"))

except:
    try:
        pg_creds = json.load(open(expanduser('~')+'/keys/postgreDB.json'))
    except:
        pg_creds = []

try:
    pg_creds = [pg_creds['dbname'], pg_creds['user'], pg_creds['password'], pg_creds['host'], pg_creds['port']]
    # pg_creds = [pg_creds['new_dbname'], pg_creds['new_user'], pg_creds['new_password'], pg_creds['new_host'], pg_creds['new_port']]
except:
    pg_creds = []
try:
    l3_dir ="/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/db1.sqlite3"
except:
    l3_dir = os.path.dirname(os.getcwd()) + "/db1.sqlite3"

# -----ALL TASKS-----
# upload_lpt
# download_lpt
# update_map_rows
# blogSync
# adSync
# log_lpt
# update_current_popularity
# hardcoded_scrape #debug
# testruntast #debug

try:
    servername = open("/home/bitnami/keys/servername.txt").readline()
except:
    try:
        servername = open(expanduser("~")+"/keys/servername.txt").readline()

    except:
        print("ERROR: SERVERNAME NOT FOUND")
        CELERY_BEAT_SCHEDULE = {}



UPDATE_CITY_TASKS = {
        'UPDATE_VANCOUVER_POPULARITY':{
            'task': 'update_current_popularity',
            'schedule': crontab(minute="0-59/10"),
            'args': ("Canada", "vancouver", 'America/Vancouver', False, False, p, 16), #arguments to pass to the function goes here
        },

        'UPDATE_SEATTLE_POPULARITY':{
            'task': 'update_current_popularity',
            'schedule': crontab(minute="1-59/10"),
            'args': ("", "seattle", 'America/Vancouver', False, False, p, 16), #US address include country
        },

        'UPDATE_VICTORIA_POPULARITY':{
            'task': 'update_current_popularity',
            'schedule': crontab(minute='2-59/10'),
            'args': ("Canada", "victoria", "America/Vancouver", False, False, p, 16), #US address include country
        },

        'UPDATE_GTA_POPULARITY':{
            'task': 'update_current_popularity',
            'schedule': crontab(minute='3-59/10'),
            'args': ("Canada", "toronto", "America/Vancouver", False, False, p, 16), #US address include country
        },

        'UPDATE_SILICON_VALLEY_POPULARITY':{
            'task': 'update_current_popularity',
            'schedule': crontab(minute='4-59/10'),
            'args': ("", "silicon_valley", "America/Vancouver", False, False, p, 16), #US address include country
        },

        'UPDATE_LAS_VEGAS_POPULARITY':{
            'task': 'update_current_popularity',
            'schedule': crontab(minute='5-59/10'),
            'args': ("", "las_vegas", "America/Vancouver", False, False, p, 16), #US address include country
        },

        'UPDATE_MONTREAL_POPULARITY':{
            'task': 'update_current_popularity',
            'schedule': crontab(minute='6-59/10'),
            'args': ("Canada", "montreal", "America/Montreal", False, False, p, 16), #US address include country
        },

        # 'UPDATE_NEW_YORK_POPULARITY':{
        #     'task': 'update_current_popularity',
        #     'schedule': crontab(minute='7-59/10'),
        #     'args': ("", "new_york", "America/Toronto", False, False, p, 16), #US address include country
        # },


}

COMMON_TASKS = {
            'SYNC_BLOG': {
                'task': 'blogSync',
                'schedule': crontab(minute='*/15'),
                'args': (pg_creds, l3_dir),
                },
            'SYNC_ADS': {
                'task': 'adSync',
                'schedule': crontab(minute='*/15'),
                'args': (pg_creds, l3_dir),
                },
            'UPDATE_MAP_ROWS': {
                'task': 'update_map_rows',
                'schedule': crontab(minute='*/15'),
                'args': (pg_creds, l3_dir),
            },
        }

OS_TASKS = {
        'DOWNLOAD_LPT':{
            'task': 'download_lpt',
            'schedule': crontab(minute="*/3"),
            'args': (pg_creds, l3_dir), #arguments to pass to the function goes here
        },
}


BS_TASKS = {
        'LOG_LPT':{
            'task': 'log_lpt',
            'schedule': crontab(minute='5-59/10'),
            'args' : (pg_creds,),
        },

        'UPLOAD_LPT': {
            'task': 'upload_lpt',
            'schedule': crontab(minute='*/5'),
            'args': (pg_creds, l3_dir),
        },

        'UPDATE_BLOG_ROWS': {
            'task': 'update_blog_rows',
            'schedule': crontab(minute='0'),
            'args': (pg_creds, l3_dir),
        },

        'UPDATE_MAP_ROWS': {
            'task': 'update_map_rows',
            'schedule': crontab(minute='*/15'),
            'args': (pg_creds, l3_dir),
        },
    }

if ("DEV" in servername):
    CELERY_BEAT_SCHEDULE = {}
    CELERY_BEAT_SCHEDULE.update(COMMON_TASKS)
    # CELERY_BEAT_SCHEDULE.update(UPDATE_CITY_TASKS)
    # print(CELERY_BEAT_SCHEDULE)


elif ("BS" in servername):
    CELERY_BEAT_SCHEDULE = {}
    CELERY_BEAT_SCHEDULE.update(BS_TASKS)
    CELERY_BEAT_SCHEDULE.update(COMMON_TASKS)
    CELERY_BEAT_SCHEDULE.update(UPDATE_CITY_TASKS)


elif ("OS" in servername):
    CELERY_BEAT_SCHEDULE = {}
    CELERY_BEAT_SCHEDULE.update(OS_TASKS)
    CELERY_BEAT_SCHEDULE.update(COMMON_TASKS)

else:
    print("SEVERNAME NOT FOUND")
    CELERY_BEAT_SCHEDULE={}



"""
TIMEZONES:
'America/Vancouver': Seattle, Victoria, Portland, Los Angeles, San Franciso, San Diego,
'America/Toronto' : New York, Toronto/GTA
'America/Montreal': Montreal


"""


