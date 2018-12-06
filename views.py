import requests
import json

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from maintainer_site.serializers import ProjectSerializer
from maintainer_site.models.models import Project


class BlogsView(APIView):
    """
    """

    def get(self, request, format=None):
        """
        """

        response = requests.get("https://medium.com/img-iit-roorkee/latest/?format=json")
        required_data_posts = [
            "id",
            "creatorId",
            "title",
            "createdAt",
            "slug",
            "subtitle",
            "imageId",
            "readingTime",
        ]
        required_response = []
        content = response.content
        text = content[16:]
        blogs = json.loads(text).get('payload')
        for blog in blogs.get('posts'):
            required_content = {}
            for j in required_data_posts:
                required_content[j] = blog.get(j)
                if (not required_content[j]):
                    required_content[j] = blog.get('virtuals').get(j) or blog.get('virtuals').get('previewImage').get(j)
            user = blogs.get('references').get('User').get(required_content['creatorId'])
            required_content['name'] = user.get('name')
            required_content['authorImageId'] = user.get('imageId')
            required_response.append(required_content)                    
        return Response(required_response)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing all the Projects
    """

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

