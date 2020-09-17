from rest_framework import serializers
from maintainer_site.models.maintainer_info import MaintainerInformation

from kernel.serializers.person import AvatarSerializer
from kernel.serializers.roles.maintainer import MaintainerSerializer
from formula_one.serializers.generics.social_information import (
    SocialInformationSerializer,
)
from formula_one.mixins.period_mixin import ActiveStatus


class MaintainerInfoSerializer(serializers.ModelSerializer):
    """
    Serializer maintainer information model
    """

    maintainer = MaintainerSerializer(
        read_only=True,
    )
    social_information = SocialInformationSerializer(
        source='maintainer.person.social_information',
        many=True,
        read_only=True,
    )
    is_alumni = serializers.SerializerMethodField()

    def get_is_alumni(self, obj):
        """
        Returns whether the maintainer is an alumni
        :returns: whether the maintainer is an alumni
        """

        active_status = obj.maintainer.active_status
        return active_status == ActiveStatus.HAS_BEEN_ACTIVE

    class Meta:
        """
        Meta class for MaintainerInfoSerializer
        """

        model = MaintainerInformation
        exclude = [
            'datetime_created',
            'datetime_modified',
        ]
        read_only_fields = [
            'maintainer',
        ]
