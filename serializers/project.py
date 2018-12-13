from rest_framework import serializers
from maintainer_site.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        """
        """

        model = Project
        exclude = [
            'datetime_created',
            'datetime_modified',
        ]
