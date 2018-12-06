from rest_framework import routers
from django.urls import path, include
from maintainer_site.views import BlogsView
from maintainer_site.views import ProjectViewSet

router = routers.SimpleRouter()
router.register('project', ProjectViewSet, base_name='project')

urlpatterns = [
        path('blogs/', BlogsView.as_view()),
        path('', include(router.urls)),
]
