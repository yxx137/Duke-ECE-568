# Generated by Django 4.0.1 on 2022-01-28 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookaride', '0004_alter_request_number_passengers_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='number_passengers_total',
            field=models.IntegerField(default=1),
        ),
    ]
