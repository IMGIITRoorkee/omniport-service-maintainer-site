import json

from rest_framework import viewsets
from rest_framework.response import Response

from maintainer_site.serializers.project import ProjectSerializer
from maintainer_site.models import Project


class MaintainerProjectView(viewsets.ModelViewSet):
    """
    A viewset for viewing all the projects of the current maintainer
    """

    serializer_class = ProjectSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Return queryset of projects worked on by the current maintainer
        :return: queryset of projects worked on by the current maintainer
        """

        maintainer_id = self.kwargs["maintainer_id"]
        return Project.objects.filter(members=maintainer_id)
