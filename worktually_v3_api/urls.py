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
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.views import VerifyOTPView

schema_view = get_schema_view(
    openapi.Info(
        title="Employee API",
        default_version="v1",
        description="API documentation for Employee management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@employees.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("employee.urls")),
    path("api/recruitment/", include("recruitment.urls")),
    path("api/", include("recruitment.jobseeker_recruitment.job_search.urls")),
    path("api/", include("recruitment.jobseeker_recruitment.apply_to_job.urls")),
    path("api/", include("recruitment.jobseeker_recruitment.accept_reject_joboffer.urls")),
    path("api/", include("recruitment.jobseeker_recruitment.accept_reject_interview.urls")),
    path(
        "api/", include("recruitment.organization_recruitment.search_candidates.urls")
    ),
    path(
        "api/",
        include("recruitment.organization_recruitment.send_interview_request.urls"),
    ),
    path(
        "api/", include("recruitment.organization_recruitment.shortlist_candidate.urls")
    ),
    path("api/", include("recruitment.organization_recruitment.send_joboffer.urls")),
    path("api/", include("recruitment.organization_recruitment.hire_candidate.urls")),
    path("api/", include("lookups.urls")),
    path("api/", include("job_seekers.modules.accounts.urls")),
    path("api/job_seeker/", include("job_seekers.modules.job_seeker.urls")),
    path("api/education/", include("job_seekers.modules.education.urls")),
    path("api/language/", include("job_seekers.modules.languages.urls")),
    path("api/job_profile/", include("job_seekers.modules.job_profiles.urls")),
    path("api/", include("job_seekers.modules.job_profiles.urls")),
    path("api/experience/", include("job_seekers.modules.experience.urls")),
    path("api/skill/", include("job_seekers.modules.skills.urls")),
    path("api/", include("job_seekers.modules.job_assessment.urls")),
    path("api/", include("job_seekers.modules.job_interviews.urls")),
    path("api/", include("lookups.modules.states.urls")),
    path("api/", include("lookups.modules.cities.urls")),
    path("api/", include("lookups.modules.countries.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
