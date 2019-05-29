from rest_framework import serializers

from maintainer_site.models import MaintainerGroup


class MaintainerGroupSerializer(serializers.ModelSerializer):
    """
    Serializer class for MaintainerGroup
    """

    class Meta:
        """
        Meta class for MaintainerGroupSerializer
        """

        model = MaintainerGroup
        fields = [
            'name',
            'medium_slug',
            'description',
        ]
