from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config


class Culture(Model):
    """
    This model holds information about culture at IMG
    """
    
    TAG_CHOICES = [
        ('misc', 'Miscellaneous'),
        ('photoshoot', 'Photoshoot'), 
        ('chaapo', 'Chaapo'),
        ('winter_trip', 'Winter Trip'),
        ('festival', 'Festival'),
        ('farewell', 'Farewell'),
    ]

    title = models.CharField(
        max_length=127,
    )
    
    description = models.TextField(
        blank=True,
    )
    
    tag = models.CharField(
        max_length=63,
        choices=TAG_CHOICES,
        default='misc',
    )
    
    cover_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'culture'),
    )
    
    class Meta:
        """
        Meta class for CultureMemory
        """
        verbose_name_plural = 'culture memories'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        return f'{self.title} ({self.tag})'