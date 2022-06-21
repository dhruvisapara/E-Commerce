from rest_framework import permissions
from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):
    message = "only staff members  can update or delete category."

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class User_cart_permission(BasePermission):
    """only user can update or delete their cart."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class User_business_permission(BasePermission):
    """only business user can update or delete company products"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.business_customer == request.user
