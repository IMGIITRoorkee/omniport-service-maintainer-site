from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.serializers.project_maintainer import ProjectMaintainerCreateUpdateSerializer, ProjectMaintainerDetailSerializer
from maintainer_site.models.project_maintainer import ProjectMaintainer


class ProjectMaintainerViewSet(viewsets.ModelViewSet):
    """
    API endpoint allows ProjectMaintainerModel to be viewed or edited
    - GET /project-maintainers/ (list)
    - POST /project-maintainers/ (create) 
    - GET /project-maintainers/{id}/ (retrieve)
    - PUT/PATCH /project-maintainers/{id}/ (update)
    - DELETE /project-maintainers/{id}/ (delete)
    """

    queryset = ProjectMaintainer.objects.all()
    pagination_size = 12

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action
        """
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectMaintainerCreateUpdateSerializer
        else:
            return ProjectMaintainerDetailSerializer
        

    def get_permissions(self):
        """
        Prohibit unauthenticated and non-maintainers to update, edit or delete
        a project
        """

        permission_classes = []
        if self.request.method not in SAFE_METHODS:
            permission_classes = [
                IsAuthenticated & get_has_role('Maintainer', ActiveStatus.ANY)
            ]
        return [permission() for permission in permission_classes]
    
