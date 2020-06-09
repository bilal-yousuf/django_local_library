from django.contrib import admin

from .models import CurrentAlbum
# Register your models here.
@admin.register(CurrentAlbum)
class CurrentAlbum(admin.ModelAdmin):
	list_display = ('id', 'title', 'artist', 'year')
