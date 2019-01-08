from rest_framework import serializers
from maintainer_site.models.maintainer_info import MaintainerInformation

from kernel.serializers.generics.social_information import SocialInformationSerializer
from kernel.serializers.person import AvatarSerializer
from kernel.serializers.roles.maintainers import MaintainerSerializer

class MaintainerInfoSerializer(serializers.ModelSerializer):
    """
    """
    
    maintainer = MaintainerSerializer(
        read_only=True,
    )
    social_information = SocialInformationSerializer(
        source='maintainer.person.social_information',
        many=True,
        read_only=True,
    )
    
    class Meta:
        """
        """
        model = MaintainerInformation
        exclude = [
            'datetime_created',
            'datetime_modified',
        ]
        read_only_fields = [
            'maintainer',
        ]

