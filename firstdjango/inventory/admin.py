from django.contrib import admin

from .models import Item
from .models import StudySessions

class ItemAdmin(admin.ModelAdmin):
	list_display = ['title', 'dueDate']
	
class StudySessionsAdmin(admin.ModelAdmin):
	list_display = ['date', 'timeSpent']

admin.site.register(Item, ItemAdmin)
admin.site.register(StudySessions, StudySessionsAdmin)