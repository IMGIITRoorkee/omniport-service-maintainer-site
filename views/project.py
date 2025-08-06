from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.serializers.project import ProjectListSerializer, ProjectDetailSerializer, ProjectCreateUpdateSerializer
from maintainer_site.models.project import Project


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint allows ProjectModel to be viewed or edited
    - GET /projects/ (list)
    - POST /projects/ (create) 
    - GET /projects/{id}/ (retrieve)
    - PUT/PATCH /projects/{id}/ (update)
    - DELETE /projects/{id}/ (delete)
    """

    queryset = Project.objects.all().order_by('-datetime_created')
    pagination_size = 12 
    
    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action
        """
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'retrieve':
            return ProjectDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectDetailSerializer

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
