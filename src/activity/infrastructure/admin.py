"""Django admin registrations for the activity bounded context."""

from django.contrib import admin

from activity.models import ActivityEntry, MileageEntry, Platform

admin.site.register(Platform)
admin.site.register(ActivityEntry)
admin.site.register(MileageEntry)
