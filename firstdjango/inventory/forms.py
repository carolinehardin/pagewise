from django import forms
import datetime
from inventory.models import Item, StudySessions, Course
#from django.core.exceptions import ValidationError

class newReadingForm(forms.ModelForm): 
	title = forms.CharField(label='Name of Reading', help_text="Title of the reading", required=True)
	startPage = forms.IntegerField(label='Start Page', help_text="Start Page", required=True)
	endPage = forms.IntegerField(label='End Page', help_text="End Page", required=True)
	dueDate = forms.DateField(label="Due Date",help_text="Due Date mm/dd/yyyy",  required=True)
	course = forms.ModelChoiceField(queryset=Course.objects.all().order_by('id'),  help_text="What course is this for?", required=True)
	
	class Meta:
		model = Item
		fields = ('title','startPage', 'endPage', 'dueDate', 'course')
	

class newSessionForm(forms.ModelForm): 
	date = forms.DateField(label="Date Completed",help_text="Date you did the study session", initial=datetime.date.today, required=True)
	startPage = forms.IntegerField(label='Start Page', help_text="Start Page", required=True)
	endPage = forms.IntegerField(label='End Page', help_text="What was the last page you read", required=True)
	timeSpent = forms.IntegerField(label='Minutes spent reading', help_text="How many minutes did you spend reading?", required=True)

	reading = forms.ModelChoiceField(queryset=Item.objects.all().order_by("-dueDate"), to_field_name="title", help_text="What reading did you work on?", required=True)

	class Meta:
		model = StudySessions
		fields = ('date','startPage', 'endPage', 'timeSpent', 'reading')
		
		
	
