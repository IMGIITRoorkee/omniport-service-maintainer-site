from kernel.admin.site import omnipotence

from maintainer_site.models.models import Project, MaintainerGroup

omnipotence.register(Project)
omnipotence.register(MaintainerGroup)
