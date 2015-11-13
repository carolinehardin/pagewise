from django import forms
from inventory.models import Item, StudySessions, Course
#from django.core.exceptions improt ValidationError

class newReadingForm(forms.ModelForm): 
	title = forms.CharField(label='Name of Reading', help_text="Title of the reading", required=True)
	pageStart = forms.IntegerField(label='Start Page', help_text="Start Page", required=True)
	endPage = forms.IntegerField(label='length', help_text="Number of pages", required=True)
	dueDate = forms.DateField(label="Due Date",help_text="Due Date", required=True)
	course = forms.CharField(widget=forms.HiddenInput(), initial="1")
	
	class Meta:
		model = Item
		fields = ('title','pageStart', 'endPage', 'dueDate', 'course')
	
