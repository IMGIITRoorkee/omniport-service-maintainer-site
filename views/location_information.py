from django.http import Http404

from rest_framework import generics

from maintainer_site.models import MaintainerGroup
from kernel.serializers.generics.location_information import LocationInformationSerializer

class LocationInformationView(generics.RetrieveAPIView):
    serializer_class = LocationInformationSerializer

    def get_object(self, *args, **kwargs):
        try:
            return MaintainerGroup.objects.get(pk=1).location_information.all()[0]
        except IndexError:
            raise Http404
