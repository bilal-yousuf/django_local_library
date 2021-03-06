import datetime

from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre, BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404, FileResponse, HttpResponse
from django.urls import reverse

from catalog.forms import RenewBookModelForm, RequestBookCheckoutForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()

    #Number of books containing word "psychedelic"
    num_books_psych = Book.objects.filter(title__contains="psychedelic").count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    books = Book.objects.all()
    copies = Book.objects.annotate(num_available=Count('bookinstance')) # annotate the queryset

    

    # blogs on home page
    blogposts = BlogPost.objects.all()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_psych': num_books_psych,
        'num_visits': num_visits,
        'blogposts': blogposts,
        'copies': copies,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def cv(request):
        #return render(request, 'cv.html')
    image_data = open("cv2.pdf", mode='r')
    return HttpResponse(image_data, content_type="application/pdf")

def browse(request):
    books = Book.objects.all()
    copies = Book.objects.annotate(num_available=Count('bookinstance')) # annotate the queryset
    # zip allows me to call both in a for loop in HTML templates
    books_copies = zip(books, copies)

    context = {
        'books': books,
        'copies': copies,
        'books_copies': books_copies,
    }

    return render(request, 'browse.html', context=context)

@login_required
def my_profile(request):
    """View function for each users, individual profile."""
    # get current user data
    user = request.user
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    current_loan = BookInstance.objects.filter(status__exact='o')



    context = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'current_loan': current_loan,
        'num_current_loan': len(current_loan),
    }

    return render(request, 'my_profile.html', context=context)



def request_checkout_member(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RequestBookCheckoutForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.borrowed_on = form.cleaned_data['borrowed_on']
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('browse') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_pickup_date = datetime.date.today() + datetime.timedelta(days=3)
        proposed_return_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'borrowed_on': proposed_pickup_date,
                'due_back': proposed_return_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_request.html', context)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
	model = Book

	#def get_queryset(self):
	"""This method overrides and changes the list of records returns, a flexible tool."""
        #return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
class AuthorListView(generic.ListView):
	model = Author

class AuthorDetailView(generic.DetailView):
	model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to all users."""
	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by = 25

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o')


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(PermissionRequiredMixin ,UpdateView):
    model = Author    
    permission_required = 'catalog.can_mark_returned'

    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'

    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book    
    permission_required = 'catalog.can_mark_returned'

    fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'


    success_url = reverse_lazy('books')

class BlogListView(generic.ListView):
    model = BlogPost
    paginate_by = 10

class BlogDetailView(generic.DetailView):
	model = BlogPost

class BlogCreate(PermissionRequiredMixin, CreateView):
    model = BlogPost
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'

    

class BlogUpdate(PermissionRequiredMixin, UpdateView):
    model = BlogPost    
    permission_required = 'catalog.can_mark_returned'

    fields = '__all__'

class BlogDelete(PermissionRequiredMixin, DeleteView):
    model = BlogPost
    permission_required = 'catalog.can_mark_returned'

    success_url = reverse_lazy('blog')