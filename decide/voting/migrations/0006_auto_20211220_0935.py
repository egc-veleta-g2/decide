# Generated by Django 2.0 on 2021-12-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0005_auto_20211220_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='option_types',
        ),
        migrations.RemoveField(
            model_name='questionoption',
            name='rank_order',
        ),
        migrations.AlterField(
            model_name='question',
            name='desc',
            field=models.TextField(),
        ),
    ]
