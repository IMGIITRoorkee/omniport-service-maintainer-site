from django.http import Http404

from rest_framework import generics
from rest_framework.response import Response

from maintainer_site.models.maintainer_group import MaintainerGroup
from formula_one.serializers.generics.location_information import (
    LocationInformationSerializer,
)


class LocationInformationView(generics.RetrieveAPIView):
    """
    This views shows the location of the maintainer group
    """

    serializer_class = LocationInformationSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to concisely send the country name
        :return: the location information with the country detailq
        """
        location_information = LocationInformationSerializer(
            self.get_object()
        ).data
        response = {}
        for location_attribute in location_information.keys():
            if location_attribute == 'country_detail':
                response['country'] = \
                    location_information[location_attribute]['name']
            else:
                response[location_attribute] = \
                    location_information[location_attribute]
        return Response(response)

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
