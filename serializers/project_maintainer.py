from rest_framework import serializers
from kernel.models.roles.maintainer import Maintainer

from maintainer_site.models import ProjectMaintainer

class ProjectMaintainerDetailSerializer(serializers.ModelSerializer):
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

    
class ProjectMaintainerCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a project maintainer
    """

    class Meta:
        model = ProjectMaintainer
        fields = ['project', 'role']
        read_only_fields = ['id', 'date_joined', 'maintainer']
        
        extra_kwargs = {
            'project': {'required': True},
            'role': {'required': True},
        }
        
    # def validate(self, attrs):
    #     """
    #     Custom validation to ensure unique project-maintainer pairs
    #     """
    #     request = self.context.get('request')
    #     if request and request.user:
    #         try:
    #             maintainer = Maintainer.objects.get(user=request.user)
    #             if ProjectMaintainer.objects.filter(project=attrs['project'], maintainer=maintainer).exists():
    #                 raise serializers.ValidationError("You are already a maintainer of this project.")
    #         except Maintainer.DoesNotExist:
    #             raise serializers.ValidationError("You must be a maintainer to join projects.")

    #     return attrs
    
class ProjectMaintainerListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all maintainers assouciated with a project or all projects a maintainer is associated with
    """

    maintainer_name = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = ProjectMaintainer
        fields = [
            'id', 'project', 'maintainer_name', 'project_name', 'role', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_maintainer_name(self, obj):
        """
        Returns the name of the maintainer
        """
        return str(obj.maintainer.person) if obj.maintainer else 'Unknown Maintainer'
    
    def get_project_name(self, obj):
        """
        Returns the name of the project
        """
        return str(obj.project.title) if obj.project else 'Unknown Project'