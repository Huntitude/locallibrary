from django.http import Http404
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book, Author, BookInstance, BookLanguage, Genre

import datetime

# Create your views here.

def index(request):
    """View Function for home page of this site"""
    title = 'Home'
    # generate counts of some of the main objects.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # the 'all" is implied by default
    num_authors = Author.objects.count()
    
    # Number of visits of this view
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'title':title,
        'num_visits':num_visits,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 10
    

class BookDetailView(generic.DetailView):
    model = Book
    
    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist.')
        return render(request, 'catalog/book_detail.html', context={'book':book})


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to all."""
    raise_exception = False
    model = BookInstance
    permission_required = ('catalog.can_mark_returned')
    template_name = 'catalog/all_bookinstance_list.html'
    paginate_by: 10
    
    def get_queryset(self):
        return BookInstance.objects.all().order_by('due_back')

# Class based view author list
class AuthorListView(generic.ListView):
    model = Author

# Class based view author details
class AuthorDetailView(generic.DetailView):
    model = Author
    
    def author_age(request, primary_key):
        author = Author.objects.get(pk=primary_key)
        context = {'author':author}
        return render(request, 'catalog/author_detail.html', context=context)
    

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
    


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author

# Author CRUD
class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_birth': '02/11/2001', 'date_of_death': '11/02/2021'}
    
class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

# Book CRUD
class BookCreate(CreateView):
    model = Book
    fields = ['title', 'summary', 'isbn', 'genre', 'language']
    


class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'summary', 'isbn', 'genre', 'language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
