# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-19 08:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0017_question_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='appraisal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='achievements.Appraisal'),
        ),
    ]