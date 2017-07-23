from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import admin

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
         return ('%s %s' % (self.first_name , self.last_name))


class FamilyMember(models.Model):
    profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)

    def __str__(self):
        return self.profile.first_name

class UserLink(models.Model):
	anchor = models.CharField(max_length=10000, null=True, blank=True)
	url = models.CharField(max_length=10000, null=True, blank=True)
	user = models.ForeignKey(User, null=True, blank=True)

	def __str__(self):
		return self.anchor

admin.site.register(Profile)
admin.site.register(FamilyMember)
admin.site.register(UserLink)

class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	RANK_CHOICES = ('JR','Junior'),('SP','Superior'),('HR','Human Resource')
	rank = models.CharField(max_length=2, default='JR', choices=RANK_CHOICES)

	def __str__(self):
		return ('{0} -- {1}'.format(self.rank, self.user.username))


class Appraisal(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee')
	superior = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='superior')
	# question = models.ManyToManyField(Question)
	total = models.PositiveIntegerField()
	created = models.DateField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.employee.user.username + ' ' + str(self.created)

	def get_absolute_url(self):
		return reverse('appraisal:appraisal_detail', kwargs={'pk': self.pk})


class Question(models.Model):
	appraisal = models.ForeignKey(Appraisal, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=300)
	description = models.CharField(max_length=300)
	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	RANK =(ONE, 1),(TWO, 2),(THREE, 3),(FOUR, 4),(FIVE, 5),

	rank = models.IntegerField(choices=RANK, default=ONE)
	created = models.DateField(auto_now_add=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('appraisal:question_detail', kwargs={'pk': self.pk})


