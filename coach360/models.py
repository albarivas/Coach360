from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class Survey(models.Model):
	title = models.CharField(max_length=255)
	users = models.ManyToManyField(User,related_name='surveys')
	def __unicode__(self):
		return self.title

class Question(models.Model):
	question = models.CharField(max_length=255)
	survey = models.ForeignKey(Survey)
	def __unicode__(self):
		return self.question
	
class Response(models.Model):
	question = models.ForeignKey(Question)
	from_user = models.ForeignKey(User)
	to_user = models.ForeignKey(User, related_name="responses")
	response = models.IntegerField()
	def __unicode__(self):
		return self.response