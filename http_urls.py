from rest_framework import routers
from django.urls import path, include
from maintainer_site.views.blog import BlogsView
from maintainer_site.views.project import ProjectViewSet
from maintainer_site.views.social_information import SocialInformationView
from maintainer_site.views.location_information import LocationInformationView
from maintainer_site.views.contact_information import ContactInformationView

router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, base_name='project')

urlpatterns = [
        path('blogs/', BlogsView.as_view()),
        path('social/', SocialInformationView.as_view()),
        path('location/', LocationInformationView.as_view()),
        path('contact/', ContactInformationView.as_view()),
        path('', include(router.urls)),
]
