from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, BookLanguage, Genre

from datetime import datetime

# Create your views here.

def index(request):
    """View Function for home page of this site"""
    title = 'Local Library - Home'
    # generate counts of some of the main objects.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # the 'all" is implied by default
    num_authors = Author.objects.count()
    
    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    
    # context_object_name = 'book_list' # name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Grabs 5 books containing the title 'war'
    # template_name = 'books/books_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    
    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist.')
        return render(request, 'catalog/book_detail.html', context={'book':book})
    
    
    
class AuthorListView(generic.ListView):
    model = Author
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
    def author_age(request, primary_key):
        author = Author.objects.get(pk=primary_key)
        context = {'author':author}
        return render(request, 'catalog/author_detail.html', context=context)
        
    