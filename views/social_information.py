from django.http import Http404

from rest_framework import generics

from maintainer_site.models.maintainer_group import MaintainerGroup
from formula_one.serializers.generics.social_information import (
    SocialInformationSerializer,
)


class SocialInformationView(generics.RetrieveAPIView):
    """
    This views shows the social of the maintainer group
    """

    serializer_class = SocialInformationSerializer

    def get_object(self, *args, **kwargs):
        """
        Return the social information of maintainer group
        :return: the social information of maintainer group
        """

        try:
            return MaintainerGroup.objects.get(pk=1) \
                .social_information.all()[0]
        except IndexError:
            raise Http404
