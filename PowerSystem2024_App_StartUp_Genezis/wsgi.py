"""
WSGI config for PowerSystem2024_App_StartUp_Genezis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PowerSystem2024_App_StartUp_Genezis.settings')

application = get_wsgi_application()
