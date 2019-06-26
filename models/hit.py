import swapper

from django.db import models
from formula_one.models.base import Model

from maintainer_site.models import MaintainerInformation


class Hit(Model):
    """
    This model holds the logs of the number of profile views of a maintainer
    """

    maintainer_information = models.OneToOneField(
        to=MaintainerInformation,
        on_delete=models.CASCADE,
    )

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        maintainer_information = self.maintainer_information
        views = self.views
        return f'{maintainer_information}: {views}'
