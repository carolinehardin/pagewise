from django.shortcuts import render
from django.http import Http404

from inventory.models import Item
from inventory.models import StudySessions
from inventory.models import Course

def index(request):
	items = Item.objects.all()
	studySessions = StudySessions.objects.all()
	course = Course.objects.all()
	totalMinSpent = 0
	totalPgRead = 0
	for studySession in studySessions
		studySession.date
		totalPgRead|add:studySession.pagesRead
		totalMinSpent|add:studySession.timeSpent				
	readingSpeed = totalMinSpent|add:totalPgRead
	return render(request, 'inventory/index.html', {
		'items': items,
		'studySessions': studySessions,
		'course': course,
		'readingSpeed': readingSpeed,
	})

def item_detail(request, id):
	try:
		item = Item.objects.get(id=id)
	except Item.DoesNotExist:
		raise Http404('This item does not exist')
	return render(request, 'inventory/item_detail.html', {
		'item': item,
	})
	
def studySession_detail(request, id):
	try:
		studySession = StudySessions.objects.get(id=id)
	except StudySessions.DoesNotExist:
		raise Http404('This study sessions does not exist')
	return render(request, 'inventory/studySession_detail.html', {
		'studySession': studySession,
	})
	
def course_detail(request, id):
	try:
		course = Course.objects.get(id=id)
	except Course.DoesNotExist:
		raise Http404('This course does not exist')
	return render(request, 'inventory/course_detail.html', {
		'course': course,
	})