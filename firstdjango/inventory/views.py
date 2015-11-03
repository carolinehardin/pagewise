from django.shortcuts import render
from django.http import Http404

from inventory.models import Item
from inventory.models import StudySessions

def index(request):
	items = Item.objects.all()
	studySessions = StudySessions.objects.all()
	return render(request, 'inventory/index.html', {
		'items': items,
		'studySessions': studySessions,
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