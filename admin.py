from omniport.admin.site import omnipotence
from django.contrib import admin

from maintainer_site.models import (
    Project,
    MaintainerGroup,
    MaintainerInformation,
    Hit,
    Blog,
)

omnipotence.register(Project)
omnipotence.register(MaintainerGroup)
omnipotence.register(MaintainerInformation)
omnipotence.register(Hit)
omnipotence.register(Blog)
