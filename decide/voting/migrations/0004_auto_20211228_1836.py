# Generated by Django 2.0 on 2021-12-28 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20211228_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='poll',
            field=models.NullBooleanField(default=None, verbose_name='Quick poll'),
        ),
    ]
