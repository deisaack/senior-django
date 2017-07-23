# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-19 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0019_userlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('relationship', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='familymember',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='achievements.Profile'),
        ),
    ]