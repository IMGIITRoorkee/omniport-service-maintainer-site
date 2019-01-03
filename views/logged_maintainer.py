import swapper
from rest_framework.viewsets import ModelViewSet
from maintainer_site.serializers.maintainer_info import MaintainerInfoSerializer
from maintainer_site.models.maintainer_info import MaintainerInformation
from kernel.managers.get_role import get_role
from kernel.permissions.has_role import get_has_role
from rest_framework.response import Response

class LoggedMaintainerViewSet(ModelViewSet):
    """
    API endpoint that allows MaintainerInfo Model to be viewed or edited.
    """
    permission_classes = (get_has_role('Maintainer'), )
    serializer_class = MaintainerInfoSerializer
    pagination_class = None

    def get_queryset(self):
        person = self.request.person
        queryset = MaintainerInformation.objects.filter(
                maintainer__person=person)
        return queryset

    def perform_create(self, serializer):
        """
        """

        maintainer = self.request.person.maintainer
        maintainer_info = serializer.save(maintainer=maintainer)

    def perform_update(self, serializer):
        """
        """

        maintainer = self.request.person.maintainer
        maintainer_info = serializer.save(maintainer=maintainer)

