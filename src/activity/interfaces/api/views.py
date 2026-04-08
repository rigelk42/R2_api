"""API views for the activity bounded context."""

from datetime import date

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.application.use_cases import (DeleteActivityEntry,
                                            DeleteMileageEntry)
from activity.interfaces.api.serializers import (ActivityEntrySerializer,
                                                 ActivityEntryWriteSerializer,
                                                 MileageEntrySerializer,
                                                 MileageEntryWriteSerializer,
                                                 PlatformSerializer)
from activity.models import Platform


class PlatformListView(APIView):
    """GET /api/me/platforms/ — list all available rideshare platforms."""

    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request):
        """Return all Platform records."""
        platforms = Platform.objects.all()
        return Response(PlatformSerializer(platforms, many=True).data)


class ActivityEntryListCreateView(APIView):
    """GET/POST /api/me/activity/ — list activity entries or create a new one.

    GET accepts an optional ?month=YYYY-MM query parameter; without it the
    current calendar month is used.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
        """Return activity entries for the authenticated driver.

        Filters to the month specified by the ?month=YYYY-MM query parameter,
        defaulting to the current calendar month when the parameter is absent.
        """
        driver = request.user.driver_profile
        month_param = request.query_params.get("month")

        if month_param:
            year, month = (int(part) for part in month_param.split("-"))
        else:
            today = date.today()
            year, month = today.year, today.month

        entries = driver.activity_entries.filter(date__year=year, date__month=month)

        return Response(ActivityEntrySerializer(entries, many=True).data)

    def post(self, request):
        """Create a new activity entry for the authenticated driver.

        Returns the created entry with HTTP 201 on success.
        """
        serializer = ActivityEntryWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        return Response(
            ActivityEntrySerializer(entry).data, status=status.HTTP_201_CREATED
        )


class ActivityEntryDetailView(APIView):
    """PATCH/DELETE /api/me/activity/<pk>/ — update or remove a specific activity entry.

    Only entries belonging to the authenticated driver are accessible;
    attempting to access another driver's entry raises a 404.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["patch", "delete"]

    def patch(self, request, pk):
        """Update all fields of the specified activity entry."""
        entry = request.user.driver_profile.activity_entries.get(pk=pk)
        serializer = ActivityEntryWriteSerializer(
            entry, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        return Response(ActivityEntrySerializer(entry).data)

    def delete(self, request, pk):
        """Delete the specified activity entry and return HTTP 204."""
        entry = request.user.driver_profile.activity_entries.get(pk=pk)
        DeleteActivityEntry().execute(entry)

        return Response(status=status.HTTP_204_NO_CONTENT)


class MileageEntryListCreateView(APIView):
    """GET/POST /api/me/mileage/ — list mileage entries or create a new one.

    GET accepts an optional ?month=YYYY-MM query parameter to filter to a
    specific month; without it all mileage entries are returned.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
        """Return mileage entries for the authenticated driver.

        Filters to the month specified by the ?month=YYYY-MM query parameter
        when present; otherwise returns all entries.
        """
        driver = request.user.driver_profile
        month_param = request.query_params.get("month")

        entries = driver.mileage_entries.all()
        if month_param:
            entries = entries.filter(month=month_param)

        return Response(MileageEntrySerializer(entries, many=True).data)

    def post(self, request):
        """Create a new mileage entry for the authenticated driver.

        Returns the created entry with HTTP 201 on success.
        """
        serializer = MileageEntryWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        return Response(
            MileageEntrySerializer(entry).data, status=status.HTTP_201_CREATED
        )


class MileageEntryDetailView(APIView):
    """PATCH/DELETE /api/me/mileage/<pk>/ — update or remove a specific mileage entry.

    Only entries belonging to the authenticated driver are accessible;
    attempting to access another driver's entry raises a 404.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["patch", "delete"]

    def patch(self, request, pk):
        """Update all fields of the specified mileage entry."""
        entry = request.user.driver_profile.mileage_entries.get(pk=pk)
        serializer = MileageEntryWriteSerializer(
            entry, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        return Response(MileageEntrySerializer(entry).data)

    def delete(self, request, pk):
        """Delete the specified mileage entry and return HTTP 204."""
        entry = request.user.driver_profile.mileage_entries.get(pk=pk)
        DeleteMileageEntry().execute(entry)

        return Response(status=status.HTTP_204_NO_CONTENT)
