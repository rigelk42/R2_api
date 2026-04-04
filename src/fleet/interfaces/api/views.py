"""API views for the fleet bounded context."""

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from fleet.interfaces.api.serializers import (DriverProfileSerializer,
                                              VehicleSerializer,
                                              VehicleWriteSerializer)


class DriverProfileView(RetrieveUpdateAPIView):
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user.driver_profile


class VehicleListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
        driver = request.user.driver_profile
        vehicles = driver.vehicles.all()
        serializer = VehicleSerializer(vehicles, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = VehicleWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()

        return Response(VehicleSerializer(vehicle).data, status=status.HTTP_201_CREATED)


class VehicleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch", "delete"]

    def patch(self, request, pk):
        vehicle = request.user.driver_profile.vehicles.get(pk=pk)
        serializer = VehicleWriteSerializer(
            vehicle, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()

        return Response(VehicleSerializer(vehicle).data)

    def delete(self, request, pk):
        vehicle = request.user.driver_profile.vehicles.get(pk=pk)
        vehicle.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
