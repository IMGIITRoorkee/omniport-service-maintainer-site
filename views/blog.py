import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from maintainer_site.models import MaintainerGroup

class BlogsView(APIView):
    """
    """

    def get(self, request, format=None):
        """
        """
        
        group_object = MaintainerGroup.objects.get(pk=1)
        pub_id = group_object.medium_slug
        response = requests.get("https://medium.com/"+str(pub_id)+"/latest/?format=json")
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
        blog_count = 0
        total_blog = 6
        for blog in blogs.get('posts'):
            if (blog_count == total_blog):
                break
            required_content = {}
            for j in required_data_posts:
                required_content[j] = blog.get(j)
                if (not required_content[j]):
                    required_content[j] = blog.get('virtuals').get(j) or blog.get('virtuals').get('previewImage').get(j)
            user = blogs.get('references').get('User').get(required_content['creatorId'])
            required_content['name'] = user.get('name')
            required_content['authorImageId'] = user.get('imageId')
            required_response.append(required_content)
            blog_count += 1
        return Response(required_response)
