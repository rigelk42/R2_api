"""API views for the identity bounded context."""

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from identity.interfaces.api.serializers import (SignupSerializer,
                                                 UpdateUserSerializer)


class SignupView(CreateAPIView):
    """POST /api/signup/ — create a new user account.

    Open to anonymous requests. Returns a uniform success envelope
    instead of the serialized object so that password hashes and other
    internal fields are never exposed in the response.
    """

    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Validate the payload, create the user, and return a success message."""
        super().create(request, *args, **kwargs)
        return Response(
            {"detail": "Account created successfully"}, status=status.HTTP_201_CREATED
        )


class UserProfileView(RetrieveUpdateAPIView):
    """GET/PATCH /api/me/ — retrieve or update the authenticated user's profile.

    Returns and accepts given_names and surnames. Email is read-only and
    cannot be changed through this endpoint.
    """

    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        """Return the currently authenticated user as the target object."""
        return self.request.user
