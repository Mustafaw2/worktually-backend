from django.urls import path
from .views import *
from .modules.education_experience.views import *
from .modules.skills_languages_portfolio.views import *
from .modules.dependents.views import *

urlpatterns = [
    path('employees/list/', EmployeesList.as_view(), name='employees_list'),
    path('employees/add/', AddEmployee.as_view(), name='add_employee'),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name='employee_detail'),
    path('employees/<int:pk>/edit/basic/', EditBasicInformation.as_view(), name='edit_basic_information'),
    path('employees/<int:pk>/edit/work/', EditWorkInformation.as_view(), name='edit_work_information'),
    path('employees/<int:pk>/edit/personal/', EditPersonalInformation.as_view(), name='edit_personal_information'),
    path('employees/<int:pk>/edit/bank/', EditBankAccount.as_view(), name='edit_bank_account'),
    path('employees/<int:pk>/edit/emergency/', EditEmergencyInformation.as_view(), name='edit_emergency_information'),
    path('employees/experiences/list/', ExperiencesListView.as_view(), name='experiences-list'),
    path('employees/experiences/add/', AddExperienceView.as_view(), name='add-experience'),
    path('employees/experiences/edit/<int:experience_id>/', EditExperienceView.as_view(), name='edit-experience'),
    path('employees/experiences/<int:experience_id>/delete/', DeleteExperienceView.as_view(), name='delete-experience'),
    path('employees/educations/list', EducationsListView.as_view(), name='educations-list'),
    path('employees/educations/add/', AddEducationView.as_view(), name='add-education'),
    path('employees/educations/edit/<int:education_id>/', EditEducationView.as_view(), name='edit-education'),
    path('employees/educations/<int:education_id>/delete/', DeleteEducationView.as_view(), name='delete-education'),
    path('employees/dependents/list', DependentsListView.as_view(), name='dependents-list'),
    path('employees/dependents/add/', AddDependentView.as_view(), name='add-dependent'),
    path('employees/dependents/edit/<int:dependent_id>/', EditDependentView.as_view(), name='edit-dependent'),
    path('employees/dependents/<int:dependent_id>/delete/', DeleteDependentView.as_view(), name='delete-dependent'),
    path('employees/skills/list', SkillsListView.as_view(), name='skills-list'),
    path('employees/skills/add/', AddSkillView.as_view(), name='add-skill'),
    path('employees/skills/<int:skill_id>/delete/', DeleteSkillView.as_view(), name='delete-skill'),
    path('employees/<int:pk>/change-profile-picture/', ChangeProfilePicture.as_view(), name='change_profile_picture'),
    path('employees/<int:pk>/change-cover-picture/', ChangeCoverPicture.as_view(), name='change_cover_picture'),
]
