from omniport.admin.site import omnipotence
from django.contrib import admin

from maintainer_site.models import (
    Project,
    MaintainerGroup,
    MaintainerInformation,
    Hit,
    Culture,
    Album,
    ProjectMaintainer,
)

omnipotence.register(Project)
omnipotence.register(MaintainerGroup)
omnipotence.register(MaintainerInformation)
omnipotence.register(Hit)
omnipotence.register(Culture)
omnipotence.register(Album)
omnipotence.register(ProjectMaintainer)
