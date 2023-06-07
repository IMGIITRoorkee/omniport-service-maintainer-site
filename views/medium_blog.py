import re
import requests
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from maintainer_site.models import MaintainerGroup

class BlogView(APIView):
    MAX_BLOG_COUNT = 6
    MIN_BLOGS_PER_CATEGORY = 2

    def get(self, request, format=None):
        """
        Return the sanitized response of blogs fetched from the Medium API
        :return: the sanitized response of blogs fetched from the Medium API
        """

        max_blog_count = int(request.GET.get('max_blogs', self.MAX_BLOG_COUNT))
        min_blogs_per_category = int(request.GET.get('min_blogs', self.MIN_BLOGS_PER_CATEGORY))

        try:
            group_object = MaintainerGroup.objects.get(pk=1)
        except MaintainerGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        pub_id = group_object.medium_slug
        url = f"https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/{pub_id}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                blog_list = json.loads(response.content).get("items")
                required_blog_list = blog_list[:max_blog_count]

                category_dict = {"culture": [], "development": [], "design": []}
                category_counts = {"culture": 0, "development": 0, "design": 0}

                for blog in required_blog_list:
                    blog_data = self.get_sanitized_blog(blog)
                    blog_categories = blog.get("categories")

                    found_category = False
                    for category in category_dict.keys():
                        if category in blog_categories and category_counts[category] < min_blogs_per_category:
                            category_dict[category].append(blog_data)
                            category_counts[category] += 1
                            found_category = True
                            break

                    if not found_category:
                        category_dict["culture"].append(blog_data)
                        category_counts["culture"] += 1

                sanitized_response = []
                for category, blogs in category_dict.items():
                    temp = {}
                    temp['category'] = category
                    temp['blogs_list'] = blogs
                    sanitized_response.append(temp)

                return Response(sanitized_response)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except requests.exceptions.RequestException as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_sanitized_blog(blog):
        """
        Returns a dictionary of required data for a blog
        """

        required_data_posts = [
            "author",
            "title",
            "pubDate",
            "link",
            "thumbnail",
            "categories",
            "guid"
        ]
        sanitized_content = {}
        for item in required_data_posts:
            sanitized_content[item] = blog.get(item)
        tag_regex = r'>([^<]+)<'
        tag_data = re.search(tag_regex, blog.get("description"))
        if tag_data:
            sanitized_content["description"] = tag_data.group(1)
        return sanitized_content
