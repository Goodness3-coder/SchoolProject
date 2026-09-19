from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """Base permission that checks if user has one of the allowed roles."""
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "role")
            and request.user.role in self.allowed_roles
        )


class IsAdmin(RolePermission):
    allowed_roles = ["admin"]


class IsTeacher(RolePermission):
    allowed_roles = ["teacher"]


class IsStudent(RolePermission):
    allowed_roles = ["student"]


class IsParent(RolePermission):
    allowed_roles = ["parent"]


class IsAdminOrTeacher(RolePermission):
    allowed_roles = ["admin", "teacher"]


class IsAdminOrTeacherOrParent(RolePermission):
    allowed_roles = ["admin", "teacher", "parent"]
