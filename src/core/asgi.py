"""ASGI entrypoint for the R2 API.

Exposes the ASGI callable as ``application`` for use by ASGI servers
such as Uvicorn or Daphne.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_asgi_application()
