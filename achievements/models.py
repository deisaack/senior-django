from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL


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


