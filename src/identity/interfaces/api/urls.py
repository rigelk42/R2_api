from django.urls import path

from identity.interfaces.api.views import SignupView

urlpatterns = [path("signup/", SignupView.as_view(), name="signup")]
