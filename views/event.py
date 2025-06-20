from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.serializers.project import EventSerializer
from maintainer_site.models.project import Event

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint allows EventModel to be viewed or edited
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('-event_date')
    pagination_size = 12 

    def get_permissions(self):
        """
        Prohibit unauthenticated and non-maintainers to update, edit or delete
        an event
        """

        permission_classes = []
        if self.request.method not in SAFE_METHODS:
            permission_classes = [
                IsAuthenticated & get_has_role('Maintainer', ActiveStatus.ANY)
            ]
        return [permission() for permission in permission_classes]

