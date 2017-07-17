from __future__ import unicode_literals

import hashlib
import os.path
import urllib

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib import admin
User = settings.AUTH_USER_MODEL


class Employee(models.Model):
	GENDER_CHOICES = ('M', 'Male'), ('F', 'Female')
	user = models.OneToOneField(User, related_name='+')
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

	def __str__(self):
		return ('%s (%s)' % (self.user.username, self.gender))

admin.site.register(Employee)

class Superior(models.Model):
	id = models.CharField(max_length=12, primary_key=True, unique=True)
	employee = models.ForeignKey(Employee, related_name='+')

	def __str__(self):
		return self.id

class Question(models.Model):
	appraisal = models.ForeignKey('Appraisal', on_delete=models.CASCADE, related_name='appraisal')
	title = models.CharField(max_length=300)
	description = models.CharField(max_length=300)
	ONE = '1'
	TWO = '2'
	THREE = '3'
	FOUR = '4'
	FIVE = '5'
	RANK = (
		(ONE, '1'),
		(TWO, '2'),
		(THREE, '3'),
		(FOUR, '4'),
		(FIVE, '5'),
	)
	rating = models.CharField(max_length=10, choices=RANK, default=ONE)
	is_active = models.BooleanField(default=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('production:supply-detail', kwargs={'pk': self.pk})


class Appraisal(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee')
	superior = models.ForeignKey(Superior, on_delete=models.CASCADE, related_name='superior')
	question = models.ForeignKey(Question, related_name='question')
	total = models.PositiveIntegerField()
	created = models.DateField(auto_now_add=True, auto_now=False)
	ONE = '1'
	TWO = '2'
	THREE = '3'
	FOUR = '4'
	FIVE = '5'
	RANK = (
		(ONE, '1'),
		(TWO, '2'),
		(THREE, '3'),
		(FOUR, '4'),
		(FIVE, '5'),
	)
	rating = models.CharField(max_length=10, choices=RANK, default=ONE)

	def __str__(self):
		return str(self.employee)
