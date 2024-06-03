import logging
from django.http import JsonResponse
from employee.models import Role_has_Permission, Permission
from django.urls import resolve

logger = logging.getLogger(__name__)

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        required_permission = view_kwargs.get('required_permission', None)
        if required_permission and not request.user.profile.role.role_permissions.filter(permission__name=required_permission).exists():
            return JsonResponse({"message": "Forbidden: You do not have permission to perform this action."}, status=403)
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        required_permission = view_kwargs.get('required_permission', None)
        
        if required_permission:
            logger.debug(f"Required permission: {required_permission}")
            
            if not request.user.is_authenticated:
                logger.warning(f"Unauthorized access attempt to {request.path}")
                return JsonResponse({"message": "Authentication credentials were not provided."}, status=401)
            
            user_profile = getattr(request.user, 'profile', None)
            if not user_profile:
                logger.warning(f"User {request.user.id} does not have a profile assigned")
                return JsonResponse({"message": "Forbidden: You do not have permission to perform this action."}, status=403)
            
            user_role = getattr(user_profile, 'role', None)
            print(user_role)
            if not user_role:
                logger.warning(f"User {request.user.id} does not have a role assigned")
                return JsonResponse({"message": "Forbidden: You do not have permission to perform this action."}, status=403)
            
            logger.debug(f"User {request.user.id} has role {user_role}")
            
            if not self.has_permission(user_role, required_permission):
                logger.warning(f"User {request.user.id} with role {user_role} does not have permission {required_permission}")
                return JsonResponse({"message": "Forbidden: You do not have permission to perform this action."}, status=403)

        return None

    def has_permission(self, role, permission_name):
        try:
            permission = Permission.objects.get(name=permission_name)
            return Role_has_Permission.objects.filter(role=role, permission=permission).exists()
        except Permission.DoesNotExist:
            logger.error(f"Permission {permission_name} does not exist")
            return False