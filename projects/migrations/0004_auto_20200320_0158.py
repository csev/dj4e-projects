# Generated by Django 3.0.1 on 2020-03-20 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20200320_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='published',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
