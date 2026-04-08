"""Django admin registrations for the fleet bounded context."""

from django.contrib import admin

from fleet.models import Driver, Vehicle

admin.site.register(Driver)
admin.site.register(Vehicle)
