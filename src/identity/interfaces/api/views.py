"""API views for the identity bounded context."""

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from identity.interfaces.api.serializers import SignupSerializer


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
