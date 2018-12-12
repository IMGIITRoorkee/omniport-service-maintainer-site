from django.http import Http404

from rest_framework import generics

from maintainer_site.models.maintainer_group import MaintainerGroup
from maintainer_site.serializers.maintainer_group import MaintainerGroupSerializer

class MaintainerGroupView(generics.RetrieveAPIView):
    serializer_class = MaintainerGroupSerializer

    def get_object(self, *args, **kwargs):
        try:
            return MaintainerGroup.objects.get(pk=1)
        except IndexError:
            raise Http404
