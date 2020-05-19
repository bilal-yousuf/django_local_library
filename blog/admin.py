from django.contrib import admin

from .models import Post


@admin.register(Post)
class Post(admin.ModelAdmin):
	list_dislplay = ['title', 'status', 'pub_date']
	list_filter = ['pub_date']
	