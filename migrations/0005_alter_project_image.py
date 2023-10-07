# Generated by Django 4.1.5 on 2023-10-07 16:57

from django.db import migrations, models
import formula_one.utils.upload_to
import maintainer_site.models.project


class Migration(migrations.Migration):

    dependencies = [
        ('maintainer_site', '0004_blog_maintainer_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.FileField(upload_to=formula_one.utils.upload_to.UploadTo('maintainer_site', 'projects'), validators=[maintainer_site.models.project.validate_file_extension]),
        ),
    ]