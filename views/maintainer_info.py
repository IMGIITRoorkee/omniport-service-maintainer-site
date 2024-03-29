from rest_framework import viewsets

import swapper
from formula_one.enums.active_status import ActiveStatus

from maintainer_site.models.maintainer_info import MaintainerInformation
from maintainer_site.serializers.maintainer_info import (
    MaintainerInfoSerializer,
)

Maintainer = swapper.load_model('kernel', 'Maintainer')


class MaintainerInfoViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing all the Maintainer's Information
    """

    lookup_field = 'informal_handle'
    serializer_class = MaintainerInfoSerializer
    queryset = MaintainerInformation.objects.all()


class ActiveMaintainerInfoViewSet(MaintainerInfoViewSet):
    """
    A viewset for viewing and editing all the active Maintainer's Information
    and those who will be active in future
    """

    pagination_class = None

    def get_queryset(self):
        """
        Return queryset of active maintainers
        :return: queryset of active maintainers
        """

        active_maintainers = Maintainer.objects_filter(
            ActiveStatus.IS_ACTIVE | ActiveStatus.WILL_BE_ACTIVE,
        ).all()
        queryset_map = MaintainerInformation.objects.filter(
            maintainer__in=active_maintainers,
        )
        ordered_queryset = queryset_map.order_by(
            '-maintainer__person__student__current_year',
            '-maintainer__person__student__current_semester',
            'maintainer__person__full_name',
        )
        return ordered_queryset


class InactiveMaintainerInfoViewSet(MaintainerInfoViewSet):
    """
    A viewset for viewing and editing all the Maintainer's Information who
    were active
    """

    pagination_size = 12

    def get_queryset(self):
        """
        Return queryset of inactive maintainers
        :return: queryset of inactive maintainers
        """
        inactive_maintainers = Maintainer.objects_filter(
            ActiveStatus.HAS_BEEN_ACTIVE,
        ).all()
        queryset_map = MaintainerInformation.objects.filter(
            maintainer__in=inactive_maintainers,
        )
        ordered_queryset = queryset_map.order_by(
            '-maintainer__end_date',
            'maintainer__person__full_name',
        )
        return ordered_queryset
