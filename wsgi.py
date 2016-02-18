# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ironman.settings")

from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)



