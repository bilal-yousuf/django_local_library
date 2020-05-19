from django.urls import path
from . import views

urlpatterns = [
	path('', views.BlogPostListView.as_view(), name='blog-list'),
	path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
	path('notes/', views.NotePostListView.as_view(), name='note-list'),
	path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
	
]