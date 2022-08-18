"""
WSGI config for helfa_aux_dev project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import os
import sys
sys.path.append('/var/www/django/helfa_aux/helfa_aux_dev')
sys.path.append('/var/www/django/helfa_aux')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helfa_aux_dev.settings')

application = get_wsgi_application()
