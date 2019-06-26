from rest_framework import serializers

from omniport.utils import switcher

from maintainer_site.models import Hit

MaintainerSerializer = switcher.load_serializer('kernel', 'Maintainer')


class HitSerializer(serializers.ModelSerializer):
    """
    Serializer for hit model
    """

    maintainer_name = serializers.CharField(
        source='maintainer_information.maintainer.person.full_name',
        read_only=True,
    )

    class Meta:
        """
        Meta class for HitSerializer
        """

        model = Hit
        fields = [
            'maintainer_name',
            'maintainer_information',
            'views',
        ]
        read_only_fields = ['views']
