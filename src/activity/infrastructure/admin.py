from django.contrib import admin

from activity.models import ActivityEntry, MileageEntry, Platform

admin.site.register(Platform)
admin.site.register(ActivityEntry)
admin.site.register(MileageEntry)
