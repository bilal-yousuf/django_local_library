from django.shortcuts import render
from django.views import generic
from blog.models import Post

# Create your views here.
class BlogPostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name='blogpost_list.html'

    
    queryset = Post.objects.filter(status__exact='b').all()

    
class BlogDetailView(generic.DetailView):
	model = Post
	template_name='blogpost_detail.html'

class NotePostListView(generic.ListView):
    model = Post
    paginate_by = 10
    template_name='notepost_list.html'

    
    queryset = Post.objects.filter(status__exact='n').all()

    
class NoteDetailView(generic.DetailView):
	model = Post
	template_name='notepost_detail.html'
