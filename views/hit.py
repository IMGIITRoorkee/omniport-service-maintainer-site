import swapper
from rest_framework.viewsets import ModelViewSet

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.models import Hit
from maintainer_site.serializers.hit import HitSerializer


class HitViewSet(ModelViewSet):
    """
    API endpoint listing views of a maintainer
    """
    permission_classes = (
        get_has_role('Maintainer',ActiveStatus.IS_ACTIVE) | 
        get_has_role('Maintainer',ActiveStatus.HAS_BEEN_ACTIVE),
    )
    serializer_class = HitSerializer
    queryset = Hit.objects.all()
    
    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 12
        return super().list(request, *args, **kwargs)
