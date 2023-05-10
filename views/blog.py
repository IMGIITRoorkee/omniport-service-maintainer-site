import requests
import re
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
        blog_list = json.loads(response.content).get("items")
        max_blog_count = 6
        if response.status_code == 200:
            required_blog_list = blog_list[:max_blog_count]
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        category_dict = {"culture": [], "development": [], "design": []}
        sanitized_response = BlogView.tag_segregator(required_blog_list, category_dict)
        two_for_each = BlogView.tag_count_checker(sanitized_response)

        while two_for_each == False:
            required_blog_list = blog_list[max_blog_count: (max_blog_count+6)]
            sanitized_response = BlogView.tag_segregator(required_blog_list, category_dict)
            two_for_each = BlogView.tag_count_checker(sanitized_response)
        return Response(sanitized_response)

    def tag_count_checker(sanitized_response):
        """
        Function to find whether each category has atleast 2 blogs to display
        """

        for i in range(len(sanitized_response)):
            if len(sanitized_response[i]["blogs_list"]) < 2:
                return False
        return True
    
    def tag_segregator(required_blog_list, category_dict):
        """
        Function to segregate the blogs into design, development and culture tags
        """

        categories = ["design", "development"]
        for blog in required_blog_list:
            found_tag = False
            for tag in categories:
                blog_data = BlogView.get_sanitized_blog(blog)
                if tag in blog["categories"]:
                    category_dict[tag].append(blog_data)
                    found_tag = True
            if not found_tag: 
                category_dict["culture"].append(blog_data)
                    
        sanitized_response = []
        for category, blogs in category_dict.items():
            temp = {}
            temp['category'] = category
            temp['blogs_list'] = blogs
            sanitized_response.append(temp)

        return sanitized_response

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
        ]
        sanitized_content = {}
        for item in required_data_posts:
            sanitized_content[item] = blog.get(item)
        tag_regex = r'>([^<]+)<'
        tag_data = re.search(tag_regex, blog.get("description"))
        if tag_data:
            sanitized_content["description"] = tag_data.group(1)
        return sanitized_content