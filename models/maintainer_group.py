import swapper
import datetime

from django.contrib.contenttypes import fields as contenttypes_fields
from django.conf import settings
from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo


class MaintainerGroup(Model):
    """
    This model holds the information of the maintainer group like contact
    information,address,etc.
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
        to='formula_one.ContactInformation',
        related_query_name='maintainer_group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    social_information = contenttypes_fields.GenericRelation(
        to='formula_one.SocialInformation',
        related_query_name='maintainer_group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    location_information = contenttypes_fields.GenericRelation(
        to='formula_one.LocationInformation',
        related_query_name='maintainer_group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )

    def save(self, *args, **kwargs):
        """
        Save the new object on the existing MaintainerGroup object
        """

        self.pk = 1
        self.datetime_created = datetime.datetime.now()
        self.name = settings.MAINTAINERS.text.name
        self.homepage = settings.MAINTAINERS.text.home_page or ''
        self.acronym = settings.MAINTAINERS.text.acronym or ''

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """

        return self.name
