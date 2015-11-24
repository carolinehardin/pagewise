from django.shortcuts import render
from django.http import Http404

from inventory.models import Item
from inventory.models import StudySessions
from inventory.models import Course

from inventory.forms import newReadingForm
from inventory.forms import newSessionForm

def index(request):
	items = Item.objects.all()
	studySessions = StudySessions.objects.all()
	course = Course.objects.all()
	totalMinSpent = 0
	totalPgRead = 0
	for oneSession in studySessions:
		totalPgRead = totalPgRead+oneSession.pagesRead
		totalMinSpent = totalMinSpent+oneSession.timeSpent					
	readingSpeed = round(float(totalPgRead)/float(totalMinSpent), 2)
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
	
def add_reading(request):
	# A HTTP POST?
    if request.method == 'POST':
        form = newReadingForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
           
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = newReadingForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'inventory/add_reading.html', {'form': form})

def add_session(request):
	# A HTTP POST?
    if request.method == 'POST':
        form = newSessionForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
          
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = newSessionForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'inventory/add_session.html', {'form': form})
