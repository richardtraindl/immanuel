"""import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "immanuel.settings")

application = get_wsgi_application()"""

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise

application = get_wsgi_application()
application = WhiteNoise(application, root='static') # '/path/to/static/files'
#application.add_files('/path/to/more/static/files', prefix='more-files/')