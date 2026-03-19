from django.contrib import admin

from activity.models import ActivityEntry, Platform

admin.site.register(Platform)
admin.site.register(ActivityEntry)
