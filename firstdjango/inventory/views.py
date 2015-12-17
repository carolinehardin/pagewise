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
		totalPgRead = totalPgRead+oneSession.endPage-oneSession.startPage
		totalMinSpent = totalMinSpent+oneSession.timeSpent					
	readingSpeed = round(float(totalPgRead)/float(totalMinSpent)*60, 2)
	
	for oneReading in items:
		
		#calculate percent read
		percentRead = 0
		pagesRead = 0
		
		#find all matching study sessions
		justMatchedSessions = StudySessions.objects.filter(reading = oneReading.id)
		
		#for each matching study session, count up the number of pages read
		for oneSession in justMatchedSessions:
			pagesRead = pagesRead + oneSession.endPage-oneSession.startPage
		
		#save the percent read to the reading	
		oneReading.percentRead = round(float(pagesRead) / float(oneReading.endPage - oneReading.startPage), 2)* 100
	
	return render(request, 'inventory/index.html', {
		'items': items,
		'studySessions': studySessions,
		'course': course,
		'readingSpeed': readingSpeed,
	})

def item_detail(request, id):
	try:
		item = Item.objects.get(id=id)
		percentRead = 0
		pagesRead = 0
		minutesSpent = 0
		justMatchedSessions = StudySessions.objects.filter(reading=id)
		for oneSession in justMatchedSessions:
			pagesRead = pagesRead + oneSession.endPage-oneSession.startPage
			minutesSpent = minutesSpent + oneSession.timeSpent
		percentRead = round(float(pagesRead) / float(item.endPage - item.startPage), 2)* 100
		if minutesSpent == 0:
			rateOfReading = 0
		else: 
			rateOfReading = round(float(pagesRead) / float(minutesSpent), 2)
		
	except Item.DoesNotExist:
		raise Http404('This item does not exist')
	return render(request, 'inventory/item_detail.html', {
		'item': item,
		'percentRead': percentRead,
		'pagesRead' : pagesRead,
		'minutesSpent' : minutesSpent,
		'rateOfReading' : rateOfReading,
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
		items = Item.objects.all()
		studySessions = StudySessions.objects.all()
		course = Course.objects.all()
		totalMinSpent = 0
		totalPgRead = 0
		
		course = Course.objects.get(id=id)
		courseItems = Item.objects.filter(course=id)
		percentRead = 0
		
		for oneReading in courseItems:
			pagesRead = 0
			justMatchedSessions = StudySessions.objects.filter(reading=oneReading.id)
			for oneSession in justMatchedSessions:
				pagesRead = pagesRead + oneSession.endPage-oneSession.startPage
			oneReading.percentRead = round(float(pagesRead) / float(oneReading.endPage - oneReading.startPage), 2)* 100			
	except Course.DoesNotExist:
		raise Http404('This course does not exist')
	return render(request, 'inventory/course_detail.html', {
		'course': course,
		'courseItems': courseItems,
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
