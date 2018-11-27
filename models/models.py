import swapper
import datetime

from django.db import models
from kernel.models.root import Model
from tinymce.models import HTMLField

from kernel.utils.upload_to import UploadTo


class Project(Model):
    """
    This model holds the information about a project of the maintainers
    """

    title = models.CharField(
        max_length=127,
    )
    
    members = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Maintainer'),
        blank=False,
    )

    short_description = models.TextField(
        max_length=255, 
        blank=True
    )
    long_description = HTMLField()
    
    image = models.ImageField(
        upload_to=UploadTo('maintainer_site', 'projects')
    )

    url = models.URLField(
        null=True,
    )

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """

        return self.title


class MaintainerGroup(Model):
    """
    This model holds the information of the maintianer group like contact information,address,etc.
    """
    
    group = models.OneToOneField(
        to=swapper.get_model_name('groups', 'Group'),
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        """
        saves the new object on the existing maintainerGroup object
        """

        self.pk = 1
        self.datetime_created = datetime.datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """

        return str(self.group)
