from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import AllowAny

from maintainer_site.models.maintainer_group import MaintainerGroup
from formula_one.serializers.generics.contact_information import (
    ContactInformationSerializer,
)


class ContactInformationView(generics.RetrieveAPIView):
    """
    This views shows the contact information of the maintainer group
    """

    permission_classes = [AllowAny]

    serializer_class = ContactInformationSerializer

    def get_object(self, *args, **kwargs):
        """
        Return contact information of maintainer group
        :return: contact information of maintainer group
        """

        try:
            return MaintainerGroup.objects.get(pk=1) \
                .contact_information.all()[0]
        except IndexError:
            raise Http404
