"""
ASGI config for PowerSystem2024_App_StartUp_Genezis project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PowerSystem2024_App_StartUp_Genezis.settings')

application = get_asgi_application()
