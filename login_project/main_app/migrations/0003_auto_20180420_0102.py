# Generated by Django 2.0.4 on 2018-04-20 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_fileupmodel_upload_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupmodel',
            name='upload_size',
            field=models.FloatField(default=0),
        ),
    ]
