"""API views for the activity bounded context."""

from datetime import date

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.application.use_cases import DeleteActivityEntry
from activity.interfaces.api.serializers import (ActivityEntrySerializer,
                                                 ActivityEntryWriteSerializer,
                                                 PlatformSerializer)
from activity.models import Platform


class PlatformListView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request):
        platforms = Platform.objects.all()
        return Response(PlatformSerializer(platforms, many=True).data)


class ActivityEntryListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get(self, request):
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
        serializer = ActivityEntryWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        return Response(
            ActivityEntrySerializer(entry).data, status=status.HTTP_201_CREATED
        )


class ActivityEntryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch", "delete"]

    def patch(self, request, pk):
        entry = request.user.driver_profile.activity_entries.get(pk=pk)
        serializer = ActivityEntryWriteSerializer(
            entry, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        return Response(ActivityEntrySerializer(entry).data)

    def delete(self, request, pk):
        entry = request.user.driver_profile.activity_entries.get(pk=pk)
        DeleteActivityEntry().execute(entry)

        return Response(status=status.HTTP_204_NO_CONTENT)
