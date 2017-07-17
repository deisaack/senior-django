# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-13 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0010_auto_20170712_1029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='rank',
            new_name='rating',
        ),
        migrations.AddField(
            model_name='question',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.RemoveField(
            model_name='appraisal',
            name='question',
        ),
        migrations.AddField(
            model_name='appraisal',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='achievements.Question'),
            preserve_default=False,
        ),
    ]
