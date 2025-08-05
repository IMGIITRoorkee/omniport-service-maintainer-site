from rest_framework import serializers

from maintainer_site.models import Project
from maintainer_site.serializers.project_maintainer import ProjectMaintainerSerializer

class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing projects with additional fields
    """

    maintainer_count = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for ProjectListSerializer
        """
        
        model = Project
        fields = [
            'id', 'slug', 'title', 'short_description', 'image', 'logo', 'github_link', 'website_link', 'time_published', 'is_featured', 'maintainer_count',
        ]
        
    def get_maintainer_count(self, obj):
        """
        Returns the count of maintainers associated with the project
        """
        return obj.project_maintainers.count()

class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of a project
    """

    project_maintainers = ProjectMaintainerSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for ProjectDetailSerializer
        """
        
        model = Project
        fields = [
            'id', 'slug', 'title', 'short_description', 'long_description', 'image', 'logo', 'github_link', 'website_link', 'time_published',  'is_featured', 'project_maintainers',
        ]
        read_only_fields = [
            'datetime_created',
            'datetime_modified',
        ]

class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a project
    """

    class Meta:
        """
        Meta class for ProjectCreateUpdateSerializer
        """

        model = Project
        fields = [
            'slug', 'title', 'short_description', 'long_description', 'image', 'logo', 'github_link', 'website_link', 'time_published', 'is_featured',
        ]
        read_only_fields = ['datetime_created', 'datetime_modified']