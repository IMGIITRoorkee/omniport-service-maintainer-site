from django.http import Http404

from rest_framework import generics

from maintainer_site.models.maintainer_group import MaintainerGroup
from maintainer_site.serializers.maintainer_group import (
    MaintainerGroupSerializer,
)

from django.core.exceptions import ObjectDoesNotExist


class MaintainerGroupView(generics.RetrieveAPIView):
    """
    This view shows details of the maintainer group
    """

    serializer_class = MaintainerGroupSerializer

    def get_object(self, *args, **kwargs):
        """
        Return object of maintainer group
        :return: object of maintainer group
        """

        try:
            return MaintainerGroup.objects.get(pk=1)
        except IndexError:
            raise Http404
        except ObjectDoesNotExist:
            raise Http404
