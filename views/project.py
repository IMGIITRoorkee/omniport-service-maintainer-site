from rest_framework import viewsets
from maintainer_site.serializers.project import ProjectSerializer
from maintainer_site.models.project import Project


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing all the Projects
    """

    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('-datetime_created')
    
    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 12
        return super().list(request, *args, **kwargs)
