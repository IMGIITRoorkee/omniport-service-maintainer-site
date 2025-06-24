from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config


class Event(Model):
    """
    This model holds information about IMG-hosted events
    """

    EVENT_TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('hackathon', 'Hackathon'),
        ('project_release', 'Project Release'),
        ('recruitment', 'Recruitment'),
        ('update', 'Update'),
        ('other', 'Other'),
    ]

    title = models.CharField(
        max_length=127,
    )
    
    description = models.TextField(
        blank=True,
    )
    
    event_type = models.CharField(
        max_length=31,
        choices=EVENT_TYPE_CHOICES,
        default='other',
    )
    
    event_date = models.DateTimeField()
    
    event_end_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    
    cover_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'events'),
    )
    
    location = models.CharField(
        max_length=127,
    )
    
    registration_link = models.URLField(
        blank=True,
        null=True,
    )
    
    social_link = models.URLField(
        blank=True,
        null=True,
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text='Whether the event is featured on the maintainer site',
    )
    
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    
    date_modified = models.DateTimeField(
        auto_now=True,
    )
    
    class Meta:
        """
        Meta class for Event
        """
        verbose_name_plural = 'events'
        ordering = ['-event_date']

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        return f'{self.title} ({self.get_event_type_display()}) - {self.event_date.strftime("%d %b %Y")}'