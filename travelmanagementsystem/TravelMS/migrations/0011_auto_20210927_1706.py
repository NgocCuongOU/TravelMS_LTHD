# Generated by Django 3.2.6 on 2021-09-27 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMS', '0010_postview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postview',
            name='id',
        ),
        migrations.AlterField(
            model_name='postview',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='TravelMS.post'),
        ),
    ]
