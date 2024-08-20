from rest_framework import serializers
from job_seekers.modules.job_seeker.models import JobSeeker
from django.contrib.auth import authenticate
from .models import OTP
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ["first_name", "last_name", "email", "password", "phone"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
            "phone": {"required": True},
        }

    def create(self, validated_data):
        user = JobSeeker(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "JobSeekersLoginSerializer"

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        print("Validating data:", data)
        email = data.get("email")
        password = data.get("password")
        username_field = "email"

        if email and password:
            # Explicitly specify the custom authentication backends
            user = authenticate(request=None, email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    "Invalid email or password", code="authentication_failed"
                )
        else:
            raise serializers.ValidationError(
                "Both email and password are required", code="invalid_credentials"
            )

        data["user"] = user
        return data


class LogoutSerializer(serializers.Serializer):
    pass


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        ref_name = "JobSeekersForgetPasswordSerializer"

    def validate_email(self, value):
        if not JobSeeker.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    class Meta:
        ref_name = "JobSeekersVerifyOTPSerializer"

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")
        if not OTP.objects.filter(email=email, otp=otp, is_verified=False).exists():
            raise serializers.ValidationError("Invalid OTP.")
        return data


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        ref_name = "JobSeekerResetPasswordRequestSerializer"

    def validate(self, data):
        email = data.get("email")
        token = data.get("token")
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        if not OTP.objects.filter(email=email, reset_token=token).exists():
            raise serializers.ValidationError("Invalid or expired token.")
        return data

    def save(self):
        validated_data = self.validated_data
        otp_instance = OTP.objects.get(
            email=validated_data["email"], reset_token=validated_data["token"]
        )
        employee = JobSeeker.objects.get(email=validated_data["email"])
        employee.set_password(validated_data["new_password"])
        employee.save()
        # Invalidate the OTP and token after successful password reset
        otp_instance.delete()
        return validated_data


class JobSeekerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims based on user type
        if isinstance(user, JobSeeker):
            token["role"] = "job_seeker"

        return token
