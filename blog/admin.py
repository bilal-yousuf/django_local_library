from django.contrib import admin

from .models import Blog, Note


@admin.register(Blog)
class Blog(admin.ModelAdmin):
	list_dislplay = ['title', 'pub_date']
	list_filter = ['pub_date']
	

@admin.register(Note)
class Note(admin.ModelAdmin):
	list_dislplay = ['title', 'pub_date']
	list_filter = ['pub_date']
	