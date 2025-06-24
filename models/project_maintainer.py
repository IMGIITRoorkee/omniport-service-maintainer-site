import swapper

from django.db import models

from formula_one.models.base import Model


class ProjectMaintainer(Model):
    """
    Through table for Project <-> Maintainer many-to-many relationship,
    holding extra data like role, date joined etc..
    """

    project = models.ForeignKey(
        to='Project', 
        related_name='project',
        on_delete=models.CASCADE
    )
    
    maintainer = models.ForeignKey(
        swapper.get_model_name('kernel', 'Maintainer'),
        related_name='project_maintainer',
        on_delete=models.CASCADE
    )
    
    role = models.CharField(
        max_length=100
    )
    
    date_joined = models.DateField()

    class Meta:
        """
        Meta class for Project
        """
        
        unique_together = ('project', 'maintainer')
        verbose_name_plural = 'project_maintainers'

    def __str__(self):
        """
        Return the string representation of the object
        :return: the string representation of the object
        """
        title = self.project.title
        maintainer = self.maintainer

        return f'{title}: {maintainer} ({self.role})'
        