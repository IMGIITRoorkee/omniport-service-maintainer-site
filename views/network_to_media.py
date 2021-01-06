from shutil import copy
from os import makedirs

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus
from django_filemanager.models import Folder, FileManager

from maintainer_site.apps import Config


class NetworkToMedia(APIView):
    """
    View to copy the asset from network_files to media_files
    """

    permission_classes = [
        IsAuthenticated & get_has_role('Maintainer', ActiveStatus.ANY)
    ]
    dst_sub_directory = 'extras'

    def post(self, request):
        """
        Copies the file from network_files to media_files and returns
        the destination path in response
        """

        path = request.data.get('path', None)
        filemanager_name = request.data.get('filemanager_name', None)
        if path is None:
            return Response(
                'Invalid path provided',
                status=status.HTTP_400_BAD_REQUEST,
            )

        person = request.user.person
        app_name = Config.name
        filemanager = FileManager.objects.get(
            filemanager_name=filemanager_name)
        folder_name = filemanager.folders.get(
            person=person, parent=None).folder_name
        dst_dir = (
            f'{settings.MEDIA_ROOT}/{app_name}/'
            f'{self.dst_sub_directory}/{folder_name}'
        )

        try:
            makedirs(dst_dir)
        except FileExistsError:
            pass

        network_file_src = f'{settings.NETWORK_STORAGE_ROOT}/{path}'
        dst_path = copy(network_file_src, dst_dir)

        response_path = dst_path.replace(
            settings.MEDIA_ROOT, settings.MEDIA_URL)
        response_data = {
            'message': f'{path} moved to {dst_path}',
            'path': response_path,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
