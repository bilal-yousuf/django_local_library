from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('books/', views.BookListView.as_view(), name='books'),
	path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
	path('authors/', views.AuthorListView.as_view(), name='authors'),
	path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
	path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	path('borrowed/', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
	path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('books/create/', views.BookCreate.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog_create'),
    path('blog/<int:pk>/update/', views.BlogUpdate.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', views.BlogDelete.as_view(), name='blog_delete'),    
    path('my-profile/', views.my_profile, name='my-profile'),

]