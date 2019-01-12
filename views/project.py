from rest_framework import viewsets
from maintainer_site.serializers.project import ProjectSerializer
from maintainer_site.models.project import Project
from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated
from kernel.permissions.has_role import get_has_role



class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint allows ProjectModel to be viewed or edited
    """
   
    permission_classes = (get_has_role('Maintainer')|ReadOnly,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('-datetime_created')
    
    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 12
        return super().list(request, *args, **kwargs)
