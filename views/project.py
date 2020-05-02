from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.serializers.project import ProjectSerializer
from maintainer_site.models.project import Project


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint allows ProjectModel to be viewed or edited
    """

    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('-datetime_created')
    pagination_size = 12 

    def get_permissions(self):
        """
        Prohibit unauthenticated and non-maintainers to update, edit or delete
        a project
        """

        permission_classes = []
        if self.request.method not in SAFE_METHODS:
            permission_classes = [
                IsAuthenticated &
                (get_has_role('Maintainer', ActiveStatus.IS_ACTIVE) |
                get_has_role('Maintainer', ActiveStatus.HAS_BEEN_ACTIVE))
            ]
        return [permission() for permission in permission_classes]
