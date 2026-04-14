"""Root URL configuration for the R2 API.

Mounts the Django admin, JWT token endpoints (obtain / refresh / blacklist),
and all bounded-context API routes under the /api/ prefix.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(
        "api/token/blacklist/",
        jwt_views.TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    path("api/", include("identity.interfaces.api.urls")),
    path("api/", include("fleet.interfaces.api.urls")),
    path("api/", include("activity.interfaces.api.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
