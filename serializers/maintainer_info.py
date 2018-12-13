from rest_framework import serializers
from maintainer_site.models.maintainer_info import MaintainerInformation

from kernel.serializers.generics.social_information import SocialInformationSerializer
from kernel.serializers.person import AvatarSerializer

class MaintainerInfoSerializer(serializers.ModelSerializer):
    """
    """

    role = serializers.ReadOnlyField(
        source='maintainer.role'
    )
    designation = serializers.ReadOnlyField(
        source='maintainer.designation'
    )
    social_information = SocialInformationSerializer(
        source='maintainer.person.social_information',
        many=True,
    )
    full_name = AvatarSerializer(
        source='maintainer.person',
    )
      
    
    class Meta:
        """
        """
        model = MaintainerInformation
        exclude = [
            'datetime_created',
            'datetime_modified',
        ]

