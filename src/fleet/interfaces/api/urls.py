from django.urls import path

from fleet.interfaces.api.views import DriverProfileView

urlpatterns = [
    path("me/driver-profile/", DriverProfileView.as_view(), name="driver-profile"),
]
