from rest_framework import serializers
from kernel.models import SocialInformation

class SocialInformationSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        """
        """

        model = SocialInformation
        fields = '__all__'

