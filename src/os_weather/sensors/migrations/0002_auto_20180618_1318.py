# Generated by Django 2.0.6 on 2018-06-18 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='valuescalculatedmodel',
            unique_together={('sensor', 'signal', 'day')},
        ),
        migrations.AlterUniqueTogether(
            name='valuesmodel',
            unique_together={('sensor', 'signal', 'timestamp')},
        ),
    ]
