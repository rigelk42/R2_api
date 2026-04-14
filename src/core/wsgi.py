"""WSGI entrypoint for the R2 API.

Exposes the WSGI callable as ``application`` for use by WSGI servers
such as Gunicorn.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
