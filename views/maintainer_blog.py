import requests
import re

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from maintainer_site.models import MaintainerInformation, Blog
from maintainer_site.serializers.blog import BlogSerializer

from maintainer_site.permissions.auth_maintainer import IsMaintainer

class MaintainerBlogView(APIView):
    """
    This view shows the list of blogs published by the mainatainer group on Medium.
    """
    
    permission_classes = [IsMaintainer]
    serializer_class = BlogSerializer
    
    def get(self, request, unique_id=None):
        """
        Returns the blogs written by the maintainer when authenticated if unique_id passed, else lists all blogs
        """

        if(self.kwargs):
            try:
                try:
                    maintainer_info = MaintainerInformation.objects.get(informal_handle=unique_id)
                except:
                    return Response({"message": "Pass handle name to get blogs written by the maintainer."}, status=status.HTTP_400_BAD_REQUEST)

                blogs = Blog.objects.filter(member=maintainer_info.maintainer)
                if not blogs:
                    return Response({"message": "No blog found from the maintainer."}, status=status.HTTP_404_NOT_FOUND)
                serialized_blog = BlogSerializer(blogs, many=True)
                return Response(serialized_blog.data, status=status.HTTP_200_OK)
            except Blog.DoesNotExist:
                return Response({"message": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if(request.query_params):
                guid = request.query_params.get('guid')
                try: 
                    blog = Blog.objects.get(guid=guid)
                except Blog.DoesNotExist: 
                    return Response({"message": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND)
                serialized_blog = BlogSerializer(blog)
                return Response(serialized_blog.data, status=status.HTTP_200_OK)
            blogs = BlogSerializer(Blog.objects.all(), many=True)
            return Response(blogs.data, status=status.HTTP_200_OK)

    def filter_blogs_by_maintainer(handle_name):
        """
        Returns blogs of a maintainer from its handle name
        """

        maintainer_information = get_object_or_404(MaintainerInformation, informal_handle=handle_name)
        maintainer = maintainer_information.maintainer
        blogs = Blog.objects.filter(member=maintainer)
        return blogs

    def extract_medium_guid(self, url):
        """
        Function should return the unique identifier if found else return None for the blog url added by maintainer
        """

        url = url.strip("/")
        url = url.split("?")[0]

        match = re.search(r"/p/([^/]+)$|/([^/]+)$", url)
        if match:
            guid = match.group(1) or match.group(2)
            if '-' in guid:
                guid = guid.rsplit('-', 1)[-1]
            return guid
        return None

    def post(self, request, format=None):
        """
        Handles post request from authenticated maintainer to add, update and delete a blog
        """

        maintainer_information = MaintainerInformation.objects.get(
            informal_handle=request.data['handle_name'],
        )
        if self.request.user.is_authenticated and self.request.user.person.maintainer:
            url = request.data['url']
            guid = self.extract_medium_guid(url)
            if self.request.method == 'POST':
                if Blog.objects.filter(guid=guid).exists():
                    return Response({"message": "Blog already exists"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    blog = Blog.objects.create(
                        guid=guid,
                        url=request.data['url'],
                        title=request.data['title'],
                        member=request.user.person.maintainer,
                        display_image=request.data['display_image'],
                        read_time=request.data['read_time']
                    )
                    blog.save()
                    return Response({"message": "Blog added successfully"}, status=status.HTTP_201_CREATED)

    def patch(self, request, format=None):
        if self.request.user.is_authenticated and self.request.user.person.maintainer:
            guid = request.data['guid']
            if Blog.objects.filter(guid=guid).exists():
                blog = Blog.objects.get(guid=guid)
                blog.title = request.data.get('title', blog.title)
                blog.save()
                return Response({"message": "Blog updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, unique_id=None):
        try: 
            blog = Blog.objects.get(guid=unique_id)
            blog.delete()
            return Response({"message": "Blog deleted successfully"}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"message": "Blog does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            