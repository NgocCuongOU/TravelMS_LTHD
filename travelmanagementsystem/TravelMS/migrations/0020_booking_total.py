# Generated by Django 3.2.6 on 2021-12-24 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMS', '0019_auto_20211224_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total',
            field=models.BigIntegerField(null=True),
        ),
    ]