"""API views for the fleet bounded context."""

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from fleet.interfaces.api.serializers import (DriverProfileSerializer,
                                              VehicleSerializer,
                                              VehicleWriteSerializer)


class DriverProfileView(RetrieveUpdateAPIView):
    """GET/PATCH /api/me/driver-profile/ — retrieve or update the driver profile.

    Exposes driver license information. Both license number and issuing
    state must be provided together or both left blank.
    """

    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        """Return the driver profile linked to the authenticated user."""
        return self.request.user.driver_profile


class VehicleListCreateView(APIView):
    """GET/POST /api/me/vehicles/ — list all vehicles or add a new one."""

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
        """Return all vehicles belonging to the authenticated driver."""
        driver = request.user.driver_profile
        vehicles = driver.vehicles.all()
        serializer = VehicleSerializer(vehicles, many=True)

        return Response(serializer.data)

    def post(self, request):
        """Create a new vehicle for the authenticated driver.

        Returns the created vehicle with HTTP 201 on success.
        """
        serializer = VehicleWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()

        return Response(VehicleSerializer(vehicle).data, status=status.HTTP_201_CREATED)


class VehicleDetailView(APIView):
    """PATCH/DELETE /api/me/vehicles/<pk>/ — update or remove a specific vehicle.

    Only vehicles owned by the authenticated driver are accessible;
    attempting to access another driver's vehicle raises a 404.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["patch", "delete"]

    def patch(self, request, pk):
        """Update all fields of the specified vehicle."""
        vehicle = request.user.driver_profile.vehicles.get(pk=pk)
        serializer = VehicleWriteSerializer(
            vehicle, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()

        return Response(VehicleSerializer(vehicle).data)

    def delete(self, request, pk):
        """Delete the specified vehicle and return HTTP 204."""
        vehicle = request.user.driver_profile.vehicles.get(pk=pk)
        vehicle.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
