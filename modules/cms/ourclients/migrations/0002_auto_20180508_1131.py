# Generated by Django 2.0.4 on 2018-05-08 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ourclients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ourclient',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='static/images/client'),
        ),
    ]
