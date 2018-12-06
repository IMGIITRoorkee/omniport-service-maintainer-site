import swapper
import datetime
from tinymce.models import HTMLField

from django.contrib.contenttypes import fields as contenttypes_fields
from django.db import models

from kernel.models.root import Model
from kernel.utils.upload_to import UploadTo


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


class MaintainerGroup(Model):
    """
    This model holds the information of the maintianer group like contact information,address,etc.
    """
    
    name = models.CharField(
        max_length=127,
    )
    homepage = models.URLField(
        blank=True,
    )
    acronym = models.CharField(
        max_length=63,
        blank=True,
    )

    description = models.TextField()

    medium_slug = models.CharField(
        max_length=63,
        blank=True,
    )

    contact_information = contenttypes_fields.GenericRelation(
        to='kernel.ContactInformation',
        related_query_name='maintainer_group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    social_information = contenttypes_fields.GenericRelation(
        to='kernel.SocialInformation',
        related_query_name='maintainer_group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    location_information = contenttypes_fields.GenericRelation(
        to='kernel.LocationInformation',
        related_query_name='maintainer_group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )

    def save(self, *args, **kwargs):
        """
        saves the new object on the existing maintainerGroup object
        """
        
        self.pk = 1
        self.datetime_created = datetime.datetime.now()
        
        self.name = settings.CONFIGURATION.branding.text.name
        self.homepage = settings.CONFIGURATION.branding.text.homepage
        self.acronym = settings.CONFIGURATION.branding.text.acronym
        
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """

        return self.name


