import swapper
from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config


class Blog(Model):
    """
    This model holds the information about a blog written by a maintainer
    """
    
    guid = models.SlugField(
        primary_key=True, 
        max_length=127
    )
    
    url = models.URLField(
        verbose_name='URL',
    )
    
    title = models.CharField(
        max_length=255,
        unique=True,
    )
    
    member = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Maintainer'),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    
    display_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'blogs'),
    )
    
    read_time = models.IntegerField(
        blank=False,
    )
    
    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """
        return f'{self.member.person.short_name}: {self.title}'
        