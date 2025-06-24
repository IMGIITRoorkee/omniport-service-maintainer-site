from rest_framework import serializers

from maintainer_site.models.album import Album


class AlbumSerializer(serializers.ModelSerializer):
    """
    Serializer for Album model
    """
    
    google_drive_link = serializers.URLField(source='drive_link')
    
    class Meta:
        model = Album
        fields = [
            'id',
            'title', 
            'description',
            'year',
            'cover_image',
            'google_drive_link',
        ]


class AlbumCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Album objects
    """
    
    google_drive_link = serializers.URLField(source='drive_link')
    
    class Meta:
        model = Album
        fields = [
            'title',
            'description', 
            'year',
            'cover_image',
            'google_drive_link',
        ]
        
    def validate_year(self, value):
        """
        Validate that year is reasonable
        """
        if value < 2000 or value > 2030:
            raise serializers.ValidationError("Year must be between 2000 and 2030")
        return value
