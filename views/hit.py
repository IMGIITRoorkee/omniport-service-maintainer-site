import swapper
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.models import Hit
from maintainer_site.models.maintainer_info import MaintainerInformation
from maintainer_site.serializers.hit import HitSerializer


class HitViewSet(ModelViewSet):
    """
     A viewset for viewing and editing views of a maintainer's profile
    """

    lookup_field = 'maintainer_information'
    serializer_class = HitSerializer
    queryset = Hit.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = (
                get_has_role('Maintainer', ActiveStatus.IS_ACTIVE) |
                get_has_role('Maintainer', ActiveStatus.HAS_BEEN_ACTIVE),
            )
        else:
            permission_classes = ()
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 12
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Increments profile view of a maintainer by 1
        :return: HttpResponse of 200
        """

        handle = self.kwargs['maintainer_information']
        maintainer_information = MaintainerInformation.objects.get(
            handle=handle,
        )
        hit_instance, _ = Hit.objects.get_or_create(
            maintainer_information=maintainer_information,
        )
        hit_instance.views += 1
        hit_instance.save()
        return HttpResponse(status=200)
