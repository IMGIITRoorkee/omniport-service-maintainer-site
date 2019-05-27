import swapper
from rest_framework import viewsets
from maintainer_site.serializers.maintainer_info import MaintainerInfoSerializer
from maintainer_site.models.maintainer_info import MaintainerInformation
from formula_one.enums.active_status import ActiveStatus

Maintainer = swapper.load_model('kernel', 'Maintainer')

class MaintainerInfoViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing all the Maintainer's Information
    """

    lookup_field = 'handle'
    serializer_class = MaintainerInfoSerializer
    queryset = MaintainerInformation.objects.all()
    
class ActiveMaintainerInfoViewSet(MaintainerInfoViewSet):
    """
    A viewset for viewing and editing all the active Maintainer's Information
    """

    pagination_class = None

    def get_queryset(self):
        active_maintainers = Maintainer.objects_filter(ActiveStatus.IS_ACTIVE).all()
        queryset_map = MaintainerInformation.objects.filter(
            maintainer__in=active_maintainers)
        return queryset_map


class InactiveMaintainerInfoViewSet(MaintainerInfoViewSet):
    """
    A viewset for viewing and editing all the inactive Maintainer's Information
    """

    pagination_size = 12

    def get_queryset(self):
        inactive_maintainers = Maintainer.objects_filter(ActiveStatus.IS_INACTIVE).all()
        queryset_map = MaintainerInformation.objects.filter(
            maintainer__in=inactive_maintainers)
        return queryset_map
