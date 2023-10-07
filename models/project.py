import swapper
from tinymce.models import HTMLField
from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config

import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    if ext not in allowed_extensions:
        raise ValidationError('Only JPG, JPEG, PNG, GIF, and SVG files are allowed.')


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

    image = models.FileField(
        upload_to=UploadTo(Config.name, 'projects'),
        validators=[validate_file_extension],
    )

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """

        return self.title
