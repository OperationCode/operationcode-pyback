import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyback.settings')


def pytest_configure():
    settings.DEBUG = False
    settings.RECAPTCHA_DISABLE = True

    django.setup()
