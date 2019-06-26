import swapper
from tinymce.models import HTMLField
from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo


class Project(Model):
    """
    This model holds the information about a project of the maintainers
    """

    slug = models.SlugField(
        primary_key=True,
    )

    title = models.CharField(
        max_length=127,
        unique=True,
    )

    members = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Maintainer'),
        blank=False,
    )

    short_description = models.TextField(
        max_length=255,
        blank=True,
    )
    long_description = HTMLField()

    image = models.ImageField(
        upload_to=UploadTo('maintainer_site', 'projects'),
    )

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """

        return self.title
