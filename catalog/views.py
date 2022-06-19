from django.shortcuts import render

from .models import Book, Author, BookInstance, BookLanguage, Genre

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
        'title':title
    }
    
    return render(request, 'index.html', context=context)
