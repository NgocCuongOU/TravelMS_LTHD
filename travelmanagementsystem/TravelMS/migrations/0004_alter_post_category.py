# Generated by Django 3.2.6 on 2021-08-15 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMS', '0003_rename_tag_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='post', to='TravelMS.category'),
        ),
    ]
