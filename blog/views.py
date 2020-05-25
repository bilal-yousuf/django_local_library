from django.shortcuts import render
from django.views import generic
from blog.models import Blog, Note

# Create your views here.
class BlogPostListView(generic.ListView):
    model = Blog
    paginate_by = 10
    template_name='blogpost_list.html'

    
    

    
class BlogDetailView(generic.DetailView):
	model = Blog
	template_name='blogpost_detail.html'

class NotePostListView(generic.ListView):
    model = Note
    paginate_by = 10
    template_name='notepost_list.html'

    
    
    
class NoteDetailView(generic.DetailView):
	model = Note
	template_name='notepost_detail.html'
