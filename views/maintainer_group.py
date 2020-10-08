from django.http import Http404

from rest_framework import generics

from maintainer_site.models.maintainer_group import MaintainerGroup
from maintainer_site.serializers.maintainer_group import (
    MaintainerGroupSerializer,
)


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
<<<<<<< HEAD
        except MaintainerGroup.DoesNotExist:
            raise Http404h
=======
        except IndexError:
            raise Http404
>>>>>>> parent of 668bfda... Added exception for when the maintainer group is not created 404 is raised
