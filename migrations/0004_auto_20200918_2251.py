# Generated by Django 3.0.3 on 2020-09-18 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintainer_site', '0003_auto_20200917_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintainergroup',
            name='medium_slug',
            field=models.CharField(blank=True, default='', max_length=63),
        ),
    ]
