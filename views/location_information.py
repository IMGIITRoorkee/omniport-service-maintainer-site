from django.http import Http404

from rest_framework import generics

from maintainer_site.models.maintainer_group import MaintainerGroup
from formula_one.serializers.generics.location_information import (
    LocationInformationSerializer,
)


class LocationInformationView(generics.RetrieveAPIView):
    """
    This views shows the location of the maintainer group
    """

    serializer_class = LocationInformationSerializer

    def get_object(self, *args, **kwargs):
        """
        Return the location information of maintainer group
        :return: the location information of maintainer group
        """

        try:
            return MaintainerGroup.objects.get(pk=1) \
                .location_information.all()[0]
        except IndexError:
            raise Http404
