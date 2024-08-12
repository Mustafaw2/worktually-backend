from django.urls import path
from job_seekers.modules.accounts.views import *

urlpatterns = [
    path("job_seeker/register/", RegisterView.as_view(), name="register"),
    path("job_seeker/login", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forget-password/", ForgetPasswordView.as_view(), name="forget_password"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
]
