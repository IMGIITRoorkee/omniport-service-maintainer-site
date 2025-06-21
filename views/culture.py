from django.db.models import Count, Q
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
import swapper

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus

from maintainer_site.models.culture import Culture
from maintainer_site.models.maintainer_info import MaintainerInformation
from maintainer_site.serializers.culture import (
    CultureSerializer,
    CultureCreateUpdateSerializer,
)

Maintainer = swapper.load_model('kernel', 'Maintainer')


class CultureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Culture memories
    """
    
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action
        """
        if self.action in ['create', 'update', 'partial_update']:
            return CultureCreateUpdateSerializer
        return CultureSerializer
    
    def get_permissions(self):
        """
        Return appropriate permissions based on action
        """
        if self.action == 'summary':
            return []
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [
                IsAuthenticated & get_has_role('Maintainer', ActiveStatus.IS_ACTIVE)
            ]
        else:
            permission_classes = [
                IsAuthenticated & get_has_role('Maintainer', ActiveStatus.ANY)
            ]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        """
        GET /api/culture/summary/
        Get cultural summary statistics
        """
        try:
            total_count = MaintainerInformation.objects.count()
            
            if total_count == 0:
                return Response({
                    'total_maintainers': 0,
                    'total_designers': 0,
                    'total_developers': 0,
                    'percent_anime_lovers': 0,
                    'percent_gamers': 0,
                    'percent_singers': 0,
                    'percent_cinematographers': 0,
                    'percent_windows_users': 0,
                    'percent_mac_users': 0,
                    'percent_linux_users': 0,
                    'percent_cricket_fans': 0,
                }, status=status.HTTP_200_OK)
            
            
            designers_count = MaintainerInformation.objects.filter(
                Q(maintainer__role='des') | Q(maintainer__role='duo')
            ).count()
            developers_count = MaintainerInformation.objects.filter(
                Q(maintainer__role='dev') | Q(maintainer__role='duo')
            ).count()
            
            anime_lovers_count = MaintainerInformation.objects.filter(is_anime_lover=True).count()
            gamers_count = MaintainerInformation.objects.filter(is_gamer=True).count()
            singers_count = MaintainerInformation.objects.filter(is_singer=True).count()
            cinematographers_count = MaintainerInformation.objects.filter(is_cinematographer=True).count()
            cricket_fans_count = MaintainerInformation.objects.filter(is_cricket_lover=True).count()
            
            windows_users_count = MaintainerInformation.objects.filter(os_preferences__icontains='windows').count()
            mac_users_count = MaintainerInformation.objects.filter(os_preferences__icontains='mac').count()
            linux_users_count = MaintainerInformation.objects.filter(os_preferences__icontains='linux').count()
            
            maintainer_stats = {
                'total_maintainers': total_count,
                'total_designers': designers_count,
                'total_developers': developers_count,
                'percent_anime_lovers': round((anime_lovers_count / total_count) * 100, 2),
                'percent_gamers': round((gamers_count / total_count) * 100, 2),
                'percent_singers': round((singers_count / total_count) * 100, 2),
                'percent_cinematographers': round((cinematographers_count / total_count) * 100, 2),
                'percent_windows_users': round((windows_users_count / total_count) * 100, 2),
                'percent_mac_users': round((mac_users_count / total_count) * 100, 2),
                'percent_linux_users': round((linux_users_count / total_count) * 100, 2),
                'percent_cricket_fans': round((cricket_fans_count / total_count) * 100, 2),
            }
            
            return Response(maintainer_stats, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            return Response(
                {'error': 'Unexpected failure during fetch', 'details': str(e), 'traceback': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='memories')
    def memories(self, request):
        """
        GET /api/culture/memories/
        Get all culture memories
        """
        try:
            cultures = Culture.objects.all()
            serializer = CultureSerializer(cultures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': 'Unexpected fetch failure'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request):
        """
        POST /api/culture/memories/
        Create a new culture memory
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                culture = serializer.save()
                response_serializer = CultureSerializer(culture)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {'error': 'Backend crash or DB error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def partial_update(self, request, pk=None):
        """
        PATCH /api/culture/memories/<culture_id>/
        Update a culture memory
        """
        try:
            culture = self.get_object()
            serializer = self.get_serializer(culture, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_serializer = CultureSerializer(culture)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Culture.DoesNotExist:
            return Response(
                {'error': 'Culture ID does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Server-side crash'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, pk=None):
        """
        DELETE /api/culture/memories/<culture_id>/
        Delete a culture memory and all associated albums
        """
        try:
            culture = self.get_object()
            culture_data = CultureSerializer(culture).data
            culture.delete()
            return Response(
                {'message': 'Culture memory deleted successfully', 'deleted_object': culture_data},
                status=status.HTTP_200_OK
            )
            
        except Culture.DoesNotExist:
            return Response(
                {'error': 'Culture not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Failed deletion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
