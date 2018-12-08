from kernel.admin.site import omnipotence

from maintainer_site.models.project import Project
from maintainer_site.models.maintainer_group import MaintainerGroup

omnipotence.register(Project)
omnipotence.register(MaintainerGroup)
