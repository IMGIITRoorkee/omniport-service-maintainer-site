from rest_framework import serializers

from maintainer_site.models import Event

class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for events
    """

    class Meta:
        """
        Meta class for EventSerializer
        """

        model = Event
        exclude = [
            'date_created',
            'date_modified',
        ]