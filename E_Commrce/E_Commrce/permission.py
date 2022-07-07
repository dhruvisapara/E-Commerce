from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):
    message = "only staff members  can update or delete category."

    def has_permission(self, request, view):
        """
        This permission is only for staff members.
        """
        # return request.user and request.user.is_staff
        return request.user.is_staff


class SuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        """
               This permission is only for superuser.
        """
        return request.user.is_superuser


class ModificationPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """only user can update or delete their cart."""
        return obj.user_id == request.user


class UserBusinessPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """Registered business user can only modify the company details."""
        return obj.business_customer == request.user
