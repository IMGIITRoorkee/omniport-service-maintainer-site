from kernel.admin.site import omnipotence
from django.contrib import admin

from maintainer_site.models import (
    Project,
    MaintainerGroup,
    MaintainerInformation,
)

omnipotence.register(Project)
omnipotence.register(MaintainerGroup)
omnipotence.register(MaintainerInformation)
