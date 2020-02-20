from django.contrib import admin

# Register your models here.


from .models import Author, Genre, Book, BookInstance, Language, BlogPost


class BooksInstanceInline(admin.TabularInline):
	model = BookInstance
	
    #extra = 0

@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
	list_display = ('book', 'status', 'borrower', 'due_back', 'id')
	list_filter = ('status', 'due_back')
	fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

class BooksInline(admin.TabularInline):
	model = Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BooksInstanceInline,]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

	inlines = [BooksInline]

admin.site.register(Genre)
admin.site.register(Language)

@admin.register(BlogPost)
class BlogPost(admin.ModelAdmin):
	list_display = ['title', 'pub_date']
	list_filter = ['pub_date']