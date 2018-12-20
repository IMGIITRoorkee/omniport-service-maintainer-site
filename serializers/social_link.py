from rest_framework import serializers

from kernel.models.generics.social_information import SocialLink


class SocialLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for SocialLink class
    """

    class Meta:
        """
        Meta class for SocialLink
        """

        model = SocialLink
        exclude = ('datetime_created','datetime_modified')
