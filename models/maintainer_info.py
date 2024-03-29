import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField

import swapper
from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config

from maintainer_site.constants.blog_constant import PERSONALITY_TYPES_CHOICES

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
    nick_name = models.TextField(
        max_length=255,
        null=True,
    )

    formal_biography = models.TextField(
        max_length=255,
        null=True,
    )
    informal_biography = models.TextField(
        max_length=255,
        null=True,
    )

    want_to_be = models.TextField(
        max_length=127,
        null=True,
    )

    formal_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'formal_image'),
        null=True,
    )
    childhood_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'informal_image'),
        null=True,
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

    personality_type = models.CharField(
        max_length=100, 
        choices=PERSONALITY_TYPES_CHOICES,
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

        informal_handle = self.informal_handle
        maintainer = self.maintainer
        return f'{informal_handle}: {maintainer}'
