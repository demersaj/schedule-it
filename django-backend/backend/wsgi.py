# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

application = get_wsgi_application()
