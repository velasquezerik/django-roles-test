# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20160825_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='permission',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'Show'), (2, 'Edit'), (3, 'Delete')], default=0),
        ),
        migrations.AddField(
            model_name='folder',
            name='permission',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'Show'), (2, 'Edit'), (3, 'Delete')], default=0),
        ),
        migrations.AddField(
            model_name='sharefile',
            name='permission',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'Show'), (2, 'Edit'), (3, 'Delete')], default=0),
        ),
        migrations.AddField(
            model_name='sharefolder',
            name='permission',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'Show'), (2, 'Edit'), (3, 'Delete')], default=0),
        ),
    ]