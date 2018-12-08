from rest_framework import routers
from django.urls import path, include
from maintainer_site.views.blog import BlogsView
from maintainer_site.views.project import ProjectViewSet

router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, base_name='project')

urlpatterns = [
        path('blogs/', BlogsView.as_view()),
        path('', include(router.urls)),
]
