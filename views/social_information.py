from django.http import Http404

from rest_framework import generics

from maintainer_site.models.maintainer_group import MaintainerGroup
from formula_one.serializers.generics.social_information import SocialInformationSerializer

class SocialInformationView(generics.RetrieveAPIView):
    serializer_class = SocialInformationSerializer

    def get_object(self, *args, **kwargs):
        try:
            return MaintainerGroup.objects.get(pk=1).social_information.all()[0]
        except IndexError:
            raise Http404

