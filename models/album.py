from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config


class Album(Model):
    """
    This model holds photos for a culture memory event
    """
    
    culture = models.ForeignKey(
        to='Culture',
        on_delete=models.CASCADE,
        related_name='albums',
    )
    
    title = models.CharField(
        max_length=127,
    )
    
    description = models.TextField(
        blank=True,
    )
    
    cover_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'culture_albums'),
    )
    
    drive_link = models.URLField(
        help_text='Link to the Google Drive folder containing the album photos',
    )
    
    class Meta:
        """
        Meta class for Album
        """
        verbose_name_plural = 'Culture albums'
    
    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        return f'{self.culture.title}: {self.title}'