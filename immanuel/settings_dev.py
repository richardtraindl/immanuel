"""
Local Django settings for immanuel project.
Overrides production setings
"""

import os

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.path.join('kate_db'),
    }
}

ALLOWED_HOSTS = ['127.0.0.1']

DEBUG = True
