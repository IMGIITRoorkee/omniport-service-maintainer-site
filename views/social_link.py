from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

import swapper
from kernel.managers.get_role import get_role
from kernel.permissions.has_role import get_has_role
from formula_one.models.generics.social_information import SocialLink
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.serializers.social_link import SocialLinkSerializer


class SocialLinkViewSet(ModelViewSet):
    """
    API endpoint that allows SocialLink Model to be viewed or edited.
    """
    permission_classes = (
        get_has_role('Maintainer', ActiveStatus.IS_ACTIVE) |
        get_has_role('Maintainer', ActiveStatus.HAS_BEEN_ACTIVE),
    )
    serializer_class = SocialLinkSerializer
    pagination_class = None

    def get_queryset(self):
        person = self.request.person
        if person is not None:
            socialinformation = person.social_information.filter()
        else:
            return []
        if len(socialinformation) != 0:
            queryset = SocialLink.objects.filter(
                socialinformation=socialinformation[0]
            )
        else:
            queryset = []
        return queryset

    def perform_create(self, serializer):
        """
        modifying perform_create for all the views to get Student
        instance from request
        """
        person = self.request.person
        link_instance = serializer.save()
        si, created = person.social_information.get_or_create()
        person.social_information.all()[0].links.add(link_instance)
