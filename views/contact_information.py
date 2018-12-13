from django.http import Http404

from rest_framework import generics

from maintainer_site.models.maintainer_group import MaintainerGroup
from kernel.serializers.generics.contact_information import ContactInformationSerializer

class ContactInformationView(generics.RetrieveAPIView):
    serializer_class = ContactInformationSerializer

    def get_object(self, *args, **kwargs):
        try:
            return MaintainerGroup.objects.get(pk=1).contact_information.all()[0]
        except IndexError:
            raise Http404
