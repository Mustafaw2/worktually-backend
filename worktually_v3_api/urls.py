"""
URL configuration for worktually_v3_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.views import   VerifyOTPView

schema_view = get_schema_view(
    openapi.Info(
        title="Employee API",
        default_version='v1',
        description="API documentation for Employee management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@employees.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('employee.urls')),
    path('api/recruitment/', include('recruitment.urls')),
    path("api/", include('recruitment.modules.search_candidates.urls')),
    path("api/", include('recruitment.modules.send_interview_request.urls')),
    path("api/", include('recruitment.modules.shortlist_candidate.urls')),   
    path("api/", include('recruitment.modules.send_joboffer.urls')),
    path("api/", include('recruitment.modules.hire_candidate.urls')),
]


