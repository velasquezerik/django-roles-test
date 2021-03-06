# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-11 22:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0006_auto_20160811_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Declined'), (3, 'Blocked')], default=0)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Folder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sharefolder',
            unique_together=set([('user', 'folder')]),
        ),
    ]
