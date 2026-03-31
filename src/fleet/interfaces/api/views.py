"""API views for the fleet bounded context."""

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from fleet.interfaces.api.serializers import DriverProfileSerializer


class DriverProfileView(RetrieveUpdateAPIView):
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user.driver_profile
