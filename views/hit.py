from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

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
        """
        Leave the view counter increment open to visitors and restrict every
        other action to maintainers
        :return: the permissions the action being processed requires
        """

        if self.action in ('update', 'partial_update'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [
                IsAuthenticated & get_has_role('Maintainer', ActiveStatus.ANY)
            ]
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
        maintainer_information = get_object_or_404(
            MaintainerInformation,
            handle=handle,
        )
        maintainer = getattr(self.request.person, 'maintainer', None)
        if getattr(maintainer, 'maintainerinformation', None) \
                == maintainer_information:
            return Response('Stop with the self-love :P')

        hit_instance, _ = Hit.objects.get_or_create(
            maintainer_information=maintainer_information,
        )
        hit_instance.views += 1
        hit_instance.save()
        return Response('Stalker, eh? ;)')
