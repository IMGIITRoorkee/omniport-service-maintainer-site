import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField

import swapper
from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo


class MaintainerInformation(Model):
    """
    This model holds information about the personality of a maintainer
    """

    maintainer = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Maintainer'),
        on_delete=models.CASCADE,
    )

    handle = models.SlugField(
        primary_key=True,
    )

    short_biography = models.TextField(
        max_length=255,
    )

    normie_image = models.ImageField(
        upload_to=UploadTo('maintainer_site', 'normie_image'),
    )
    dank_image = models.ImageField(
        upload_to=UploadTo('maintainer_site', 'dank_image'),
    )
    technical_skills = models.TextField(
        null=True,
    )

    """
    favourite_music = ArrayField(
        models.CharField(max_length=63, blank=True),
        size=5,
    )
    favourite_literature = ArrayField(
        models.CharField(max_length=63, blank=True),
        size=5,
    )
    favourite_video = ArrayField(
        models.CharField(max_length=63, blank=True),
        size=5,
    )
    favourite_hobbies = ArrayField(
        models.CharField(max_length=63, blank=True),
        size=5,
    )
        favourite_games = ArrayField(
        models.CharField(max_length=63, blank=True),
        size=5,
    )
    """

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
