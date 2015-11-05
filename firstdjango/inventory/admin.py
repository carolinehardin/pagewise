from django.contrib import admin

from .models import Item
from .models import StudySessions
from .models import Course

class ItemAdmin(admin.ModelAdmin):
	list_display = ['title', 'dueDate']
	
class StudySessionsAdmin(admin.ModelAdmin):
	list_display = ['date', 'timeSpent']
	
class CourseAdmin(admin.ModelAdmin):
	list_display = ['course']

admin.site.register(Item, ItemAdmin)
admin.site.register(StudySessions, StudySessionsAdmin)
admin.site.register(Course, CourseAdmin)