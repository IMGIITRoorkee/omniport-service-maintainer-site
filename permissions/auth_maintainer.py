from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from formula_one.mixins.period_mixin import ActiveStatus
from kernel.permissions.has_role import get_has_role


class IsMaintainer(BasePermission):
    """
    Custom permission class to allow access only to authenticated maintainers to update, create or delete blog
    """

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            permissions = [
                IsAuthenticated(),
                get_has_role('Maintainer', ActiveStatus.ANY)(),
            ]
            return all(permission.has_permission(request, view) for permission in permissions)
        return True
