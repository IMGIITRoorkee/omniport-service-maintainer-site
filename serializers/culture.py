from rest_framework import serializers

from maintainer_site.models.culture import Culture


class CultureSerializer(serializers.ModelSerializer):
    """
    Serializer for Culture model
    """
    
    class Meta:
        model = Culture
        fields = [
            'id',
            'title',
            'description', 
            'tag',
            'cover_image',
        ]


class CultureCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Culture objects
    """
    
    class Meta:
        model = Culture
        fields = [
            'title',
            'description',
            'tag', 
            'cover_image',
        ]

    def validate_tag(self, value):
        """
        Validate that tag is one of the allowed values
        """
        allowed_tags = ['winter_trip', 'photoshoot', 'chaapo', 'farewell', 'festival', 'misc']
        if value not in allowed_tags:
            raise serializers.ValidationError(
                f"Tag must be one of: {', '.join(allowed_tags)}"
            )
        return value
