"""URL routes for the identity bounded context."""

from django.urls import path

from identity.interfaces.api.views import SignupView, UserProfileView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("me/", UserProfileView.as_view(), name="user-profile"),
]
