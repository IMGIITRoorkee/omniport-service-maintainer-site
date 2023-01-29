import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField

import swapper
from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config


class MaintainerInformation(Model):
    """
    This model holds information about the personality of a maintainer
    """

    maintainer = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Maintainer'),
        on_delete=models.CASCADE,
    )

    informal_handle = models.SlugField(
        primary_key=True,
    )

    formal_biography = models.TextField(
        max_length=255,
    )
    informal_biography = models.TextField(
        max_length=255,
    )

    formal_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'formal_image'),
    )
    childhood_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'informal_image'),
    )
    technical_skills = models.TextField(
        null=True,
    )
    favourite_series = models.TextField(
        null=True,
    )
    favourite_sports = models.TextField(
        null=True,
    )
    personality_type = models.SlugField(
        null=True,
    )


    class Meta:
        """
        Meta class for MaintainerInformation
        """

        verbose_name_plural = 'maintainer information'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        handle = self.handle
        maintainer = self.maintainer
        return f'{handle}: {maintainer}'
