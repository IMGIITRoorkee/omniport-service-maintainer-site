from rest_framework import serializers

from maintainer_site.models import Blog
from maintainer_site.serializers.maintainer_info import (
    MaintainerInfoSerializer,
)

class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for blogs of maintainers
    """

    class Meta:
        """
        Meta class for BlogSerializer
        """

        model = Blog
        exclude = [
            'datetime_created',
            'datetime_modified',
        ]
        read_only_fields = [
            'member',
        ]
