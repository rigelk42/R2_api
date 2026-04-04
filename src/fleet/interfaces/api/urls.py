from django.urls import path

from fleet.interfaces.api.views import (DriverProfileView, VehicleDetailView,
                                        VehicleListCreateView)

urlpatterns = [
    path("me/driver-profile/", DriverProfileView.as_view(), name="driver-profile"),
    path("me/vehicles/", VehicleListCreateView.as_view(), name="vehicles"),
    path("me/vehicles/<int:pk>/", VehicleDetailView.as_view(), name="vehicle-detail"),
]
