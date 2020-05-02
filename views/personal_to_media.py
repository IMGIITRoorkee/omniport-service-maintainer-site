from shutil import copy
from os import makedirs

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from kernel.permissions.has_role import get_has_role
from formula_one.mixins.period_mixin import ActiveStatus
from django_filemanager.models import Folder

from maintainer_site.apps import Config


class PersonalToMedia(APIView):
    """
    View to copy the asset from personal_files to media_files
    """

    permission_classes = [
        IsAuthenticated & get_has_role('Maintainer', ActiveStatus.ANY)
    ]
    dst_sub_directory = 'extras'

    def post(self, request):
        """
        Copies the file from personal_files to media_files and returns
        the destination path in response
        """

        path = request.data.get('path', None)
        if path is None:
            return Response(
                'Invalid path provided',
                status=status.HTTP_400_BAD_REQUEST,
            )

        person = request.user.person
        app_name = Config.name
        folder_name = Folder.objects.get(person=person).folder_name()
        dst_dir = (
            f'{settings.MEDIA_ROOT}/{app_name}/'
            f'{self.dst_sub_directory}/{folder_name}'
        )

        try:
            makedirs(dst_dir)
        except FileExistsError:
            pass

        personal_file_src = f'{settings.PERSONAL_ROOT}/{path}' 
        dst_path = copy(personal_file_src, dst_dir)

        response_path = (
            f'{settings.MEDIA_URL}{app_name}/{self.dst_sub_directory}/'
            f'{path}'
        )

        response_data = {
            'message': f'{path} moved to {dst_path}',
            'path': response_path,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
