import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from maintainer_site.constants.tech_skills import *

class TechSkillsView(APIView):
    """
    """

    def get(self, request, format=None):
        """
        """
        print("teri ")
        with open('services/maintainer_site/static/maintainer_site/devicon/devicon.json') as directory:
            devicons = json.load(directory)
        print(devicons)
        required_response = []

        for skills in TECH_SKILLS:
            required_content = {}
            required_content["value"] = skills[0]
            required_content["text"] = skills[1]
            label_content = {}
            for devicon_object in devicons:
                if (skills[0] == devicon_object.get('name')):
                    label_content["className"] = "devicon-%s-%s"%(skills[0], devicon_object.get("versions").get("font")[0])
            required_content["label"] = label_content
            required_response.append(required_content)
        return Response(required_response)
