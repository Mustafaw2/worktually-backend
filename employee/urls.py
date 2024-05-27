from django.urls import path
from .views import *

urlpatterns = [
    path('employees/list/', EmployeesList.as_view(), name='employees_list'),
    path('employees/add/', AddEmployee.as_view(), name='add_employee'),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name='employee_detail'),
    path('employees/<int:pk>/edit/basic/', EditBasicInformation.as_view(), name='edit_basic_information'),
    path('employees/<int:pk>/edit/work/', EditWorkInformation.as_view(), name='edit_work_information'),
    path('employees/<int:pk>/edit/personal/', EditPersonalInformation.as_view(), name='edit_personal_information'),
    path('employees/<int:pk>/edit/bank/', EditBankAccount.as_view(), name='edit_bank_account'),
    path('employees/<int:pk>/edit/emergency/', EditEmergencyInformation.as_view(), name='edit_emergency_information'),
    path('experiences/', ExperiencesList.as_view(), name='experiences_list'),
    path('experiences/<int:pk>/', EditExperience.as_view(), name='edit_experience'),
    path('educations/', EducationsList.as_view(), name='educations_list'),
    path('educations/<int:pk>/', EditEducation.as_view(), name='edit_education'),
    path('dependents/', DependentsList.as_view(), name='dependents_list'),
    path('dependents/<int:pk>/', EditDependent.as_view(), name='edit_dependent'),
    path('skills/', SkillsList.as_view(), name='skills_list'),
    path('skills/<int:pk>/delete/', DeleteSkill.as_view(), name='delete_skill'),
    path('employees/<int:pk>/change-profile-picture/', ChangeProfilePicture.as_view(), name='change_profile_picture'),
    path('employees/<int:pk>/change-cover-picture/', ChangeCoverPicture.as_view(), name='change_cover_picture'),
]
