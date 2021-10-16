# Generated by Django 3.2.6 on 2021-10-15 15:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMS', '0012_auto_20211015_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tourschedules',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tourschedules',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tourschedules',
            name='travel_schedule',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
