from django.db import models

class Item(models.Model):
	title = models.CharField(max_length=200)
	startPage = models.IntegerField()
	endPage = models.IntegerField()
	course = models.CharField(max_length=200)
	dueDate = models.DateField()