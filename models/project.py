import swapper
from tinymce.models import HTMLField
from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config


class Project(Model):
    """
    This model holds the information about a projects of the maintainers
    """

    slug = models.SlugField(
        unique=True,
    )

    title = models.CharField(
        max_length=127,
        unique=True,
    )

    short_description = models.TextField(
        max_length=255,
        blank=True,
    )
    
    long_description = HTMLField()

    image = models.ImageField(
        upload_to=UploadTo(Config.name, 'project_image'),
    )
    
    logo = models.ImageField(
        upload_to=UploadTo(Config.name, 'project_logo'),
    )
    
    github_link = models.URLField(
        blank=True,
    )
    
    website_link = models.URLField(
        blank=True,
    )
    
    time_published = models.DateField()
    
    is_featured = models.BooleanField(
        default=False,
        help_text='Whether the project is featured on the maintainer site',
    )
    
    class Meta:
        """
        Meta class for Project
        """

        verbose_name_plural = 'projects'

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """

        return f"{self.id} {self.title} : {self.slug}"
