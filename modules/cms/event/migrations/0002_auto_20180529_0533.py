# Generated by Django 2.0.4 on 2018-05-29 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='detailevent',
            table='detail_highlight',
        ),
        migrations.AlterModelTable(
            name='eventgalery',
            table='cover_highlight',
        ),
    ]
