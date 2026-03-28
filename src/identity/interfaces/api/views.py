# API views for the identity bounded context.
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from identity.interfaces.api.serializers import SignupSerializer


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            {"detail": "Account created successfully"}, status=status.HTTP_201_CREATED
        )
