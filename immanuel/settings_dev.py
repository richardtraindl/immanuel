"""
Local Django settings for immanuel project.
Overrides production setings
"""

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.path.join('kate_db'),
    }
}

ALLOWED_HOSTS = ['']

DEBUG = True