# Generated by Django 2.0 on 2021-12-19 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
