# Generated by Django 3.2.6 on 2021-12-17 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMS', '0015_auto_20211217_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postview',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='post_view', serialize=False, to='TravelMS.post'),
        ),
    ]