from rest_framework import serializers
from .models import PermissionGroup, Permission, Role, Role_has_Permission



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'permission_group', 'name']



class CustomPermissionListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Map the validated data by permission ID for efficient lookup
        permission_mapping = {permission.id: permission for permission in instance}
        
        # Update existing permissions and create new ones if necessary
        updated_permissions = []
        for permission_data in validated_data:
            permission_id = permission_data.get('id')
            if permission_id is not None and permission_id in permission_mapping:
                # Update existing permission
                permission = permission_mapping[permission_id]
                permission.name = permission_data.get('name', permission.name)
                permission.save()
                updated_permissions.append(permission)
            else:
                # Create new permission
                updated_permissions.append(self.child.create(permission_data))
        
        # Return the list of updated permissions
        return updated_permissions
    

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'permission_group']
        list_serializer_class = CustomPermissionListSerializer

class PermissionGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = PermissionGroup
        fields = ['id', 'name', 'permissions']


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'name', 'created_by', 'permissions']

    def get_permissions(self, obj):
        permissions = Role_has_Permission.objects.filter(role=obj)
        return PermissionSerializer([rp.permission for rp in permissions], many=True).data

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role_has_Permission
        fields = ['id', 'role', 'permission']


class SyncPermissionsSerializer(serializers.Serializer):
    permissions = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False
    )