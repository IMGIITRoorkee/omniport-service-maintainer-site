import swapper
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from kernel.managers.get_role import get_role
from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.serializers.maintainer_info import (
    MaintainerInfoSerializer,
)
from maintainer_site.models.maintainer_info import MaintainerInformation


class LoggedMaintainerViewSet(ModelViewSet):
    """
    API endpoint that checks if a maintainer is authenticated
    """

    permission_classes = [
        IsAuthenticated &
        (get_has_role('Maintainer', ActiveStatus.IS_ACTIVE) |
        get_has_role('Maintainer', ActiveStatus.HAS_BEEN_ACTIVE))
    ]
    serializer_class = MaintainerInfoSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Return information of maintainer if authenticated
        :return: information of maintainer if authenticated
        """

        person = self.request.person
        queryset = MaintainerInformation.objects.filter(
                maintainer__person=person)
        return queryset

    def perform_create(self, serializer):
        """
        Called when new information of maintainer is registered
        """

        maintainer = self.request.person.maintainer
        maintainer_info = serializer.save(maintainer=maintainer)

    def perform_update(self, serializer):
        """
        Called when information of a maintainer is edited
        """

        maintainer = self.request.person.maintainer
        maintainer_info = serializer.save(maintainer=maintainer)
