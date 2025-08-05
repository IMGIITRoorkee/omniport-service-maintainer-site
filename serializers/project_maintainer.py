from rest_framework import serializers

from maintainer_site.models import ProjectMaintainer

class ProjectMaintainerSerializer(serializers.ModelSerializer):
    """
    Serializer for ProjectMaintainer model
    """

    maintainer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectMaintainer
        fields = [
            'id',
            'project',
            'maintainer',
            'maintainer_name',
            'role',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_maintainer_name(self, obj):
        """
        Returns the name of the maintainer
        """
        return str(obj.maintainer.person) if obj.maintainer else 'Unknown Maintainer'