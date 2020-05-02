from rest_framework import routers
from django.urls import path, include
from maintainer_site.views.blog import BlogView
from maintainer_site.views.maintainer_project import MaintainerProjectView
from maintainer_site.views.project import ProjectViewSet
from maintainer_site.views.social_information import SocialInformationView
from maintainer_site.views.location_information import LocationInformationView
from maintainer_site.views.contact_information import ContactInformationView
from maintainer_site.views.maintainer_group import MaintainerGroupView
from maintainer_site.views.maintainer_info import (
    ActiveMaintainerInfoViewSet,
    MaintainerInfoViewSet,
    InactiveMaintainerInfoViewSet,
)
from maintainer_site.views.social_link import SocialLinkViewSet
from maintainer_site.views.logged_maintainer import LoggedMaintainerViewSet
from maintainer_site.views.hit import HitViewSet
from maintainer_site.views.personal_to_media import PersonalToMedia

router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register(
    r'maintainer_project/(?P<maintainer_id>[^/.]+)',
    MaintainerProjectView,
    basename='maintainer_project',
)
router.register(
    'active_maintainer_info',
    ActiveMaintainerInfoViewSet,
    basename='active_maintainer_info',
)
router.register(
    'inactive_maintainer_info',
    InactiveMaintainerInfoViewSet,
    basename='inactive_maintainer_info',
)
router.register('social_link', SocialLinkViewSet, basename="SocialLink")
router.register(
    'logged_maintainer',
    LoggedMaintainerViewSet,
    basename="LoggedMaintainer",
)
router.register('hit', HitViewSet, basename='Hit')

urlpatterns = [
        path('blog/', BlogView.as_view()),
        path('social/', SocialInformationView.as_view()),
        path('location/', LocationInformationView.as_view()),
        path('contact/', ContactInformationView.as_view()),
        path('maintainer_group/', MaintainerGroupView.as_view()),
        path('personal_to_media/', PersonalToMedia.as_view()),
        path('', include(router.urls)),
]
