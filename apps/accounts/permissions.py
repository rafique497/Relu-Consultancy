"""
permission file
"""
from rest_framework import permissions

from apps.accounts.choice import UserType


class TeacherPermission(permissions.BasePermission):
    """
    to check if user type is teacher
    """
    def has_permission(self, request, view):
        """ return True if token user_type=teacher param """
        if request.auth.payload.get('user_type', '') == UserType.TEACHER.value:
            return True
        return False


class SuperAdminPermission(permissions.BasePermission):
    """
    to check if user type is teacher
    """
    def has_permission(self, request, view):
        """ return True if token user_type=teacher param """
        if request.auth.payload.get('user_type', '') == UserType.SUPER_ADMIN.value:
            return True
        return False
