"""URL routes for the activity bounded context."""

from django.urls import path

from activity.interfaces.api.views import (
    ActivityEntryDetailView,
    ActivityEntryListCreateView,
    ExpenseEntryDetailView,
    ExpenseEntryListCreateView,
    MileageEntryDetailView,
    MileageEntryListCreateView,
    PlatformListView,
)

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
    path("me/mileage/", MileageEntryListCreateView.as_view(), name="mileage-entries"),
    path(
        "me/mileage/<int:pk>/",
        MileageEntryDetailView.as_view(),
        name="mileage-entry-detail",
    ),
    path("me/expenses/", ExpenseEntryListCreateView.as_view(), name="expense-entries"),
    path(
        "me/expenses/<int:pk>/",
        ExpenseEntryDetailView.as_view(),
        name="expense-entry-detail",
    ),
]
