# from django.contrib import admin
# from django import forms
# from django.core.exceptions import PermissionDenied
# from .models import (
#     JobSeeker,
#     OTP,
#     # Education,
#     Language,
#     JobProfileExperience,
#     ApprovalModel,
#     JobProfile,
#     Settings,
#     JobProfileAssessment,
#     JobTitleAssessment,
#     JobProfileInterview,
#     ScreeningInterviewTemplate,
#     JobProfileInterview,
#     JobTitleAssessment,
# )
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class JobSeekerAdmin(admin.ModelAdmin):
#     list_display = ("email", "first_name", "last_name", "get_profile_completion")
#     search_fields = ("email", "first_name", "last_name")

#     def get_profile_completion(self, obj):
#         return obj.get_profile_completion()

#     get_profile_completion.short_description = "Profile Completion (%)"


# class EducationAdmin(admin.ModelAdmin):
#     list_display = ("job_seeker", "title", "education_type_id", "completion_date")
#     search_fields = ("job_seeker__email", "title")


# class LanguageAdmin(admin.ModelAdmin):
#     list_display = ("job_seeker", "language_id", "level")
#     search_fields = ("job_seeker__email", "language_id")


# class ExperienceAdmin(admin.ModelAdmin):
#     list_display = ("job_seeker", "title", "company_name", "start_date", "end_date")
#     search_fields = ("job_seeker__email", "title")


# class ApprovalModelAdmin(admin.ModelAdmin):
#     list_display = ("job_seeker", "profile_completion_percentage", "is_approved")
#     search_fields = ("job_seeker__email",)


# class ScreeningInterviewTemplateAdmin(admin.ModelAdmin):
#     list_display = ("name", "status", "added_by", "questions")
#     exclude = ("added_by",)

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # If the object is being created
#             obj.added_by = request.user  # Assign the logged-in user to added_by
#             print(f"Adding screening interview template by user: {request.user}")
#         super().save_model(request, obj, form, change)

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             form.base_fields["added_by"].queryset = User.objects.filter(
#                 pk=request.user.pk
#             )
#         return form

#     def has_add_permission(self, request):
#         # Only allow superusers to add new templates
#         return request.user.is_superuser

#     def has_change_permission(self, request, obj=None):
#         # Allow change permission only for superusers
#         return request.user.is_superuser


# admin.site.register(JobSeeker, JobSeekerAdmin)
# admin.site.register(JobProfile)
# # admin.site.register(Education, EducationAdmin)
# # admin.site.register(Language, LanguageAdmin)
# # admin.site.register(JobProfileExperience, ExperienceAdmin)
# admin.site.register(ApprovalModel, ApprovalModelAdmin)
# admin.site.register(Settings)
# admin.site.register(JobTitleAssessment)
# admin.site.register(JobProfileInterview)
# admin.site.register(JobProfileAssessment)
# admin.site.register(ScreeningInterviewTemplate)
# admin.site.register(OTP)
