from rest_framework import serializers
from maintainer_site.models import MaintainerGroup

class MaintainerGroupSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        """
        """

        model = MaintainerGroup
        fields = [
            'name',
            'medium_slug',
        ]
