import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response

from maintainer_site.models import MaintainerGroup


class BlogView(APIView):
    """
    This view shows the list of blog published by the mainatainer group on
    Medium.
    """

    def get(self, request, format=None):
        """
        Return the sanitized response of blog fetched from Medium API
        :return: the sanitized response of blog fetched from Medium API
        """

        group_object = MaintainerGroup.objects.get(pk=1)
        pub_id = group_object.medium_slug
        url = (
            "https://api.rss2json.com/v1/api.json?rss_url="
            f"https://medium.com/feed/{pub_id}"
        )
        response = requests.get(url)
        required_data_posts = [
            "author",
            "title",
            "pubDate",
            "link",
            "thumbnail",
        ]
        sanitized_response = []
        blog_list = json.loads(response.content).get("items")
        max_blog_count = 6
        if response.status_code == 200:
            required_blog_list = blog_list[:max_blog_count]
        else:
            required_blog_list = []
        for blog in required_blog_list:
            sanitized_content = {}
            for item in required_data_posts:
                sanitized_content[item] = blog.get(item)
            sanitized_response.append(sanitized_content)

        return Response(sanitized_response)
