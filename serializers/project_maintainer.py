from rest_framework import serializers
from kernel.models.roles.maintainer import Maintainer

from maintainer_site.models import ProjectMaintainer

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
        read_only_fields = ['id', 'date_joined','maintainer', 'project']

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

    
class ProjectMaintainerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a project maintainer
    """

    class Meta:
        model = ProjectMaintainer
        fields = ['project', 'role']
        
        extra_kwargs = {
            'project': {'required': True},
            'role': {'required': True},
        }
        
    def validate(self, attrs):
        """
        Prohibit creation of duplicate project maintainer combinations
        """
        request = self.context.get('request')
        if request and request.user:
            try:
                maintainer = Maintainer.objects.get(user=request.user)
                if not self.instance:
                    if ProjectMaintainer.objects.filter(project=attrs['project'], maintainer=maintainer).exists():
                        raise serializers.ValidationError("You are already a maintainer of this project.")
            except Maintainer.DoesNotExist:
                raise serializers.ValidationError("You must be a maintainer to join projects.")

        return attrs
    
class ProjectMaintainerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a project maintainer
    """

    class Meta:
        model = ProjectMaintainer
        fields = ['role']
        read_only_fields = ['project', 'maintainer', 'date_joined']
        extra_kwargs = {
            'role': {'required': True},
        }
        