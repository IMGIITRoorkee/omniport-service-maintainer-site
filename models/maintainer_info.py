import swapper

from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from maintainer_site.apps import Config


class MaintainerInformation(Model):
    """
    This model holds information about the personality of a maintainer
    """

    maintainer = models.OneToOneField(
        to=swapper.get_model_name('kernel', 'Maintainer'),
        on_delete=models.CASCADE,
    )

    handle = models.SlugField(
        primary_key=True,
    )

    short_biography = models.TextField(
        max_length=255,
    )

    normie_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'normie_image'),
    )
    
    dank_image = models.ImageField(
        upload_to=UploadTo(Config.name, 'dank_image'),
    )
    
    technical_skills = models.TextField(
        null=True,
    )
    
    is_gamer = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a gamer',
    )
    
    is_anime_lover = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is an anime lover',
    )
    
    is_singer = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a singer',
    )
    
    is_cricket_lover = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a cricket lover',
    )
    
    is_cinematographer = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a cinematographer',
    )
    
    is_windows_user = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a Windows user',
    )
    
    is_mac_user = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a Mac user',
    )
    
    is_foodie = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a foodie',
    )
    
    is_night_owl = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is a night owl',
    )
    
    is_early_bird = models.BooleanField(
        default=False,
        help_text='Whether the maintainer is an early bird',
    )

    class Meta:
        """
        Meta class for MaintainerInformation
        """

        verbose_name_plural = 'maintainer information'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        handle = self.handle
        maintainer = self.maintainer
        
        return f'{handle}: {maintainer}'
