# Generated by Django 3.2.6 on 2021-08-17 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMS', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='static/uploads/%Y/%m'),
        ),
    ]
