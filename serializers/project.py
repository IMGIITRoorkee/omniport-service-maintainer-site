from rest_framework import serializers

from maintainer_site.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for projects of maintainers
    """

    class Meta:
        """
        Meta class for ProjectSerializer
        """

        model = Project
        exclude = [
            'datetime_created',
            'datetime_modified',
        ]
