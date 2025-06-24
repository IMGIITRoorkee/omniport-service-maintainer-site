from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from django.shortcuts import get_object_or_404

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.models.culture import Culture
from maintainer_site.models.album import Album
from maintainer_site.serializers.album import (
    AlbumSerializer,
    AlbumCreateUpdateSerializer,
)


class AlbumViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Culture Albums
    """
    
    serializer_class = AlbumSerializer
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action
        """
        if self.action in ['create', 'update', 'partial_update']:
            return AlbumCreateUpdateSerializer
        return AlbumSerializer
    
    def get_permissions(self):
        """
        Return appropriate permissions based on action
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            # Only active maintainers can update/delete
            permission_classes = [
                IsAuthenticated & get_has_role('Maintainer', ActiveStatus.IS_ACTIVE)
            ]
        else:
            # List, retrieve, create require maintainer role
            permission_classes = [
                IsAuthenticated & get_has_role('Maintainer', ActiveStatus.ANY)
            ]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter albums by culture_id from URL
        """
        culture_id = self.kwargs.get('culture_id')
        return Album.objects.filter(culture_id=culture_id)
    
    def list(self, request, culture_id=None):
        """
        GET /api/culture/memories/<culture_id>/albums/
        Get all albums for a specific culture
        """
        try:
            # Verify culture exists
            culture = get_object_or_404(Culture, id=culture_id)
            albums = Album.objects.filter(culture=culture)
            
            # Try to serialize each album individually to identify problematic ones
            album_data = []
            for album in albums:
                try:
                    serializer = AlbumSerializer(album)
                    album_data.append(serializer.data)
                except Exception as album_error:
                    # Skip problematic albums and add minimal data
                    album_data.append({
                        'id': album.id,
                        'title': getattr(album, 'title', 'Unknown'),
                        'description': getattr(album, 'description', ''),
                        'year': getattr(album, 'year', 2024),
                        'cover_image': str(getattr(album, 'cover_image', '')),
                        'google_drive_link': getattr(album, 'drive_link', ''),
                    })
            
            return Response(album_data, status=status.HTTP_200_OK)
            
        except Culture.DoesNotExist:
            return Response(
                {'error': 'Culture not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Add more detailed error information for debugging
            import traceback
            return Response(
                {'error': 'Unexpected fetch failure', 'details': str(e), 'traceback': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request, culture_id=None):
        """
        POST /api/culture/memories/<culture_id>/albums/
        Create a new album under a specific culture
        """
        try:
            # Verify culture exists
            culture = get_object_or_404(Culture, id=culture_id)
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                album = serializer.save(culture=culture)
                # Return full object data with id using the read serializer
                response_serializer = AlbumSerializer(album)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Culture.DoesNotExist:
            return Response(
                {'error': 'Culture not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Backend crash or DB error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def partial_update(self, request, culture_id=None, pk=None):
        """
        PATCH /api/culture/memories/<culture_id>/albums/<album_id>/
        Update an album
        """
        try:
            # Verify culture exists
            culture = get_object_or_404(Culture, id=culture_id)
            
            # Get album and verify it belongs to the culture
            album = get_object_or_404(Album, id=pk, culture=culture)
            
            serializer = self.get_serializer(album, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Return full object data
                response_serializer = AlbumSerializer(album)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except (Culture.DoesNotExist, Album.DoesNotExist):
            return Response(
                {'error': 'Culture or Album not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Server-side crash'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, culture_id=None, pk=None):
        """
        DELETE /api/culture/memories/<culture_id>/albums/<album_id>/
        Delete an album from a culture
        """
        try:
            # Verify culture exists
            culture = get_object_or_404(Culture, id=culture_id)
            
            # Get album and verify it belongs to the culture
            album = get_object_or_404(Album, id=pk, culture=culture)
            
            album_data = AlbumSerializer(album).data
            album.delete()
            return Response(
                {'message': 'Album deleted successfully', 'deleted_object': album_data},
                status=status.HTTP_200_OK
            )
            
        except (Culture.DoesNotExist, Album.DoesNotExist):
            return Response(
                {'error': 'Culture or Album not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Failed deletion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
