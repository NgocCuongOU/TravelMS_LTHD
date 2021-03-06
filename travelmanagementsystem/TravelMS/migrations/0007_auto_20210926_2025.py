# Generated by Django 3.2.6 on 2021-09-26 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMS', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default=None, upload_to='posts/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='uploads/%Y/%m'),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('title', 'category')},
        ),
    ]
