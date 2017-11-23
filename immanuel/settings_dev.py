"""
Local Django settings for immanuel project.
Overrides production setings
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.path.join('kate_db'),
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR , 'katedb.sqlite3'),
    }
}

ALLOWED_HOSTS = ['127.0.0.1']

DEBUG = True
