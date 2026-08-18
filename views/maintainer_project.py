from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from maintainer_site.serializers.project import ProjectSerializer
from maintainer_site.models import Project


class MaintainerProjectView(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing all the projects of the current maintainer

    Projects are written through ProjectViewSet, which is gated on the
    Maintainer role
    """

    permission_classes = [AllowAny]

    serializer_class = ProjectSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Return queryset of projects worked on by the current maintainer
        :return: queryset of projects worked on by the current maintainer
        """

        maintainer_id = self.kwargs["maintainer_id"]
        return Project.objects.filter(members=maintainer_id)
