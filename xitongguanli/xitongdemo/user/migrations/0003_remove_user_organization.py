# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-08 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_operation_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
    ]
