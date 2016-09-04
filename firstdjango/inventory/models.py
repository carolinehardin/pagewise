from django.db import models

from datetime import date

class Item(models.Model):
	title = models.CharField(max_length=200)
	startPage = models.IntegerField()
	endPage = models.IntegerField()
	course = models.CharField(max_length=200)
	dueDate = models.DateField()
	
	def __unicode__(self):
		return u'{0}'.format(self.title)
	
class StudySessions(models.Model):
	date = models.DateField()
	startPage = models.IntegerField()
	endPage = models.IntegerField()
	timeSpent = models.IntegerField()	
	reading = models.ForeignKey(Item)
	
	
class Course(models.Model):
	title = models.CharField(max_length=200)
	
	def __unicode__(self):
		return u'{0}'.format(self.id)
