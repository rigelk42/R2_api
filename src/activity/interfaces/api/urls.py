from django.urls import path

from activity.interfaces.api.views import (ActivityEntryDetailView,
                                           ActivityEntryListCreateView,
                                           PlatformListView)

urlpatterns = [
    path("me/platforms/", PlatformListView.as_view(), name="platforms"),
    path(
        "me/activity/", ActivityEntryListCreateView.as_view(), name="activity-entries"
    ),
    path(
        "me/activity/<int:pk>/",
        ActivityEntryDetailView.as_view(),
        name="activity-entry-detail",
    ),
]
