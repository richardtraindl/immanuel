"""
Local Django settings for immanuel project.
Overrides production setings
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR , 'katedb.sqlite3'),
    }
}

DJANGO_SETTINGS_MODULE="settings rq worker default"

RQ_QUEUES = {
     'default': {
     'HOST': 'localhost',
     'PORT': 6379,
     'DB': 0,
     'DEFAULT_TIMEOUT': 3600,
     },
}

ALLOWED_HOSTS = ['127.0.0.1']

DEBUG = True
