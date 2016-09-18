from django.shortcuts import render
from django.http import Http404

import datetime
from datetime import datetime, timedelta

from inventory.models import Item
from inventory.models import StudySessions
from inventory.models import Course

from inventory.forms import newReadingForm
from inventory.forms import newSessionForm

def index(request):
	items = Item.objects.all().order_by('-dueDate')
	studySessions = StudySessions.objects.all()
	course = Course.objects.all().order_by('-id')
	
	totalMinSpent = 0
	totalPgRead = 0
	
	totalTimeRemaining = 0
	totalPgRemaining = 0
	
	futureDue = [] #this will save every reading due soon
	
	pastDue = [] #stuff due today or earlier
	
	#what was done (or not done!) in the last week?
	last7DaysTimeSpent = 0
	last7DaysPgRead = 0
	last7DaysPgTotal= 0
	last7DaysTimeRemaining = 0
	
	
	dueTomorrow = [] # stuff due tomorrow, used for calculating how many hours remaining work you have today
	tomorrowPgRemaining = 0
	tomorrowTimeRemaining = 0
	
	dueNext7Days = [] #what's due in next 7 days? good for planning week
	next7DaysPgRemaining = 0
	next7DaysTimeRemaining = 0
	next2WeeksTimeRemaining = 0
	
	
	now = datetime.now().date() 
	
	#we will consider tomorrow the next calendar day, not the next 24 hours. 
	#For example, if it's 3pm on Dec 1st, tomorrow is Dec 2nd, not 3pm Dec 2nd to 2:59 Dec 3rd. So strip out hours.
	tomorrow = now + timedelta(days=1)
	
	in7Days = now + timedelta(days=7) #we count today as part of the week
	last7Days = now + timedelta(days=-7)
	in2Weeks = now + timedelta(days=14)
	
	for oneSession in studySessions:
		#add one since if you read pages 1 & 2 it's 2 pages but 2-1 = 1
		totalPgRead = totalPgRead + oneSession.endPage-oneSession.startPage + 1  
		totalMinSpent = totalMinSpent + oneSession.timeSpent
		
		#add up the time and pages from last week
		if oneSession.date > last7Days:
			last7DaysTimeSpent = last7DaysTimeSpent + oneSession.timeSpent
			last7DaysPgRead = last7DaysPgRead + oneSession.endPage-oneSession.startPage +1
	
	#avoid divide by zero errors	
	if totalMinSpent > 0:					
		readingSpeed = round(float(totalPgRead)/float(totalMinSpent)*60, 2)
	else:
		readingSpeed = 0
		
	for oneReading in items:
		
		#calculate percent read
		percentRead = 0
		pagesRead = 0
		
		#calculate pages in reading
		pagesAssigned = oneReading.endPage - oneReading.startPage + 1
					
		#find all matching study sessions
		justMatchedSessions = StudySessions.objects.filter(reading = oneReading.id)
		
		#for each matching study session, count up the number of pages read
		for oneSession in justMatchedSessions:
			pagesRead = pagesRead + oneSession.endPage-oneSession.startPage +1
			
		#add pages left to total pages left
		totalPgRemaining = totalPgRemaining + pagesAssigned - pagesRead 
		
		#save the percent read to the reading	
		oneReading.percentRead = round(float(pagesRead) / float(pagesAssigned), 2)* 100
		
		#can't read more than 100%		
		if oneReading.percentRead > 100:
				oneReading.percentRead = 100
		
		#save the time remaining to read this to the reading
		oneReading.timeRemaining = round(float(pagesAssigned - pagesRead) / float(readingSpeed), 2) *60 
			
		#no negative time remaining allowed
		if oneReading.timeRemaining  < 0:
				oneReading.timeRemaining = 0
		
		#keep track of what this reading adds to total time remainig
		totalTimeRemaining = totalTimeRemaining + oneReading.timeRemaining

		#if it's due in the future
		if oneReading.dueDate > now:
			futureDue.append(oneReading)
			
			# We'd like to know tomorrow due
			if (oneReading.dueDate == tomorrow ):
				dueTomorrow.append(oneReading)
				tomorrowPgRemaining = tomorrowPgRemaining + pagesAssigned - pagesRead 
				tomorrowTimeRemaining = tomorrowTimeRemaining + oneReading.timeRemaining
			
			#is it due in the next week?
			if (oneReading.dueDate < in7Days):
				dueNext7Days.append(oneReading)
				next7DaysPgRemaining = next7DaysPgRemaining + pagesAssigned - pagesRead 
				next7DaysTimeRemaining = next7DaysTimeRemaining + oneReading.timeRemaining
				next2WeeksTimeRemaining = next2WeeksTimeRemaining + oneReading.timeRemaining
				
			#is it due in the next 2 weeks?
			elif (oneReading.dueDate < in2Weeks):
				next2WeeksTimeRemaining = next2WeeksTimeRemaining + oneReading.timeRemaining
				
		else: #else, it's due in the past
			pastDue.append(oneReading)
			
			#was it due in the last week?
			if oneReading.dueDate > last7Days:
				last7DaysPgTotal = last7DaysPgTotal + pagesAssigned 
				last7DaysTimeRemaining = last7DaysTimeRemaining + oneReading.timeRemaining
			

	
	return render(request, 'inventory/index.html', {
		'items': items,
		'studySessions': studySessions,
		'course': course,
		'readingSpeed': readingSpeed,
		'totalTimeRemaining': totalTimeRemaining,
		'totalPgRemaining': totalPgRemaining,
		'pagesAssigned': pagesAssigned,
		'totalPgRead': totalPgRead,
		'futureDue': futureDue,
		'pastDue' : pastDue,
		'tomorrow' : tomorrow,
		'tomorrowPgRemaining' : tomorrowPgRemaining,
		'tomorrowTimeRemaining' : tomorrowTimeRemaining,
		'in7Days': in7Days,
		'next7DaysPgRemaining' : next7DaysPgRemaining,
		'next7DaysTimeRemaining': next7DaysTimeRemaining,
		'next2WeeksTimeRemaining': next2WeeksTimeRemaining,
		'last7DaysPgRead':  last7DaysPgRead,		
		'last7DaysTimeSpent': last7DaysTimeSpent,
		'last7DaysTimeRemaining': last7DaysTimeRemaining,
		'last7DaysPgTotal' : last7DaysPgTotal,

	})

def item_detail(request, id):
	try:
		item = Item.objects.get(id=id)
		percentRead = 0
		pagesRead = 0
		minutesSpent = 0
		justMatchedSessions = StudySessions.objects.filter(reading=id)
		pagesAssigned = float(item.endPage - item.startPage +1 )
		
		for oneSession in justMatchedSessions:
			pagesRead = pagesRead + oneSession.endPage-oneSession.startPage +1
			minutesSpent = minutesSpent + oneSession.timeSpent
		
		#avoid div by zero errors
		if pagesRead == 0:
			percentRead = 0
		else:	
			percentRead = round(float(pagesRead) / pagesAssigned, 2)* 100
			
			#can't read more than 100%		
			if percentRead > 100:
				percentRead = 100
				
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
		'pagesAssigned': pagesAssigned,
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
		totalPagesToRead = 0
		totalPercentRead = 0
				
		course = Course.objects.get(id=id)
		courseItems = Item.objects.filter(course=id)
			
		for oneReading in courseItems:
			pagesRead = 0
			pagesToRead = float(oneReading.endPage - oneReading.startPage)
			totalPagesToRead = totalPagesToRead + pagesToRead
			
			justMatchedSessions = StudySessions.objects.filter(reading=oneReading.id) 
			for oneSession in justMatchedSessions:
				pagesRead = pagesRead + oneSession.endPage-oneSession.startPage
			
			totalPgRead = totalPgRead +pagesRead
			
			if (pagesToRead >0):
				oneReading.percentRead = round(float(pagesRead) / pagesToRead, 2)* 100
			else:
				percentRead = 100		
		
		if (totalPagesToRead >0):
			totalPercentRead = round(float(totalPgRead) / totalPagesToRead, 2)* 100	
		else:
			totalPercentRead = 100
	
	except Course.DoesNotExist:
		raise Http404('This course does not exist')
	return render(request, 'inventory/course_detail.html', {
		'course': course,
		'courseItems': courseItems,
		'totalPgRead': totalPgRead,
		'totalPercentRead': totalPercentRead,
		'totalPagesToRead': totalPagesToRead,
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
