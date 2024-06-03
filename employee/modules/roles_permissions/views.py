from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import PermissionGroup, Permission, Role, Role_has_Permission
from .serializers import PermissionGroupSerializer, PermissionSerializer, RoleSerializer, Role_has_Permission, SyncPermissionsSerializer
from django.shortcuts import get_object_or_404

class PermissionGroupsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = PermissionGroup.objects.all()
        serializer = PermissionGroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    
class AddPermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Permission added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewPermissionGroup(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            permission_group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"error": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PermissionGroupSerializer(permission_group)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddPermissionGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PermissionGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Permission group added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditPermissionGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"message": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionGroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Permission group updated successfully.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"message": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionGroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Permission group updated successfully.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditPermissionsInGroup(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, group_id):
        try:
            permission_group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"error": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)

        permissions_data = request.data.get('permissions', [])
        permission_ids = [perm.get('id') for perm in permissions_data if perm.get('id')]
        existing_permissions = permission_group.permissions.all()
        try:
            instance = Permission.objects.filter(permission_group=permission_group, id__in=permission_ids)
            serializer = PermissionSerializer(instance=existing_permissions, data=permissions_data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Permissions updated successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PermissionGroupDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"message": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionGroupSerializer(group)
        return Response(serializer.data)

class AddPermissionsToGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"message": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)

        permissions = request.data.get('permissions', [])
        if not permissions:
            return Response({"message": "No permissions provided"}, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        for perm_data in permissions:
            perm_data['permission_group'] = group.id
            serializer = PermissionSerializer(data=perm_data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Permissions added to group successfully."}, status=status.HTTP_201_CREATED)

class DeletePermissionsFromGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"message": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)

        permissions = request.data.get('permissions', [])
        Permission.objects.filter(id__in=permissions, permission_group=group).delete()
        return Response({"message": "Permissions deleted from group successfully."}, status=status.HTTP_204_NO_CONTENT)

class DeletePermissionGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_id):
        try:
            group = PermissionGroup.objects.get(id=group_id)
        except PermissionGroup.DoesNotExist:
            return Response({"message": "Permission group not found"}, status=status.HTTP_404_NOT_FOUND)

        group.delete()
        return Response({"message": "Permission group deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class RolesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class AddRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": "Role added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Role updated successfully.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Role updated successfully.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        role.delete()
        return Response({"message": "Role deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role)
        return Response(serializer.data)

class SyncPermissionsToRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        serializer = SyncPermissionsSerializer(data=request.data)
        
        if serializer.is_valid():
            permission_ids = serializer.validated_data['permissions']
            permissions = Permission.objects.filter(id__in=permission_ids)
            
            if len(permissions) != len(permission_ids):
                return Response({"message": "One or more permissions are invalid."}, status=status.HTTP_400_BAD_REQUEST)

            # Clear existing permissions
            Role_has_Permission.objects.filter(role=role).delete()

            # Add new permissions
            for permission in permissions:
                Role_has_Permission.objects.create(role=role, permission=permission)
            
            return Response({"message": "Permissions synced successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AddPermissionsToRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        permissions = request.data.get('permissions', [])
        if not permissions:
            return Response({"message": "No permissions provided"}, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        for perm_name in permissions:
            try:
                permission = Permission.objects.get(name=perm_name)
                role.role_permissions.create(permission=permission)
            except Permission.DoesNotExist:
                errors.append({"permission_name": perm_name, "error": "Permission not found"})

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Permissions added to role successfully."}, status=status.HTTP_201_CREATED)