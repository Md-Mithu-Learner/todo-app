from rest_framework.permissions import BasePermission
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return False

class HasObjAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        if request.user == obj.assignee:
            return True
        return False