
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Used to generate URLs by reversing the URL patterns.
import uuid
from datetime import date

# Create your models here.

# Model Representing a book genre
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        # String representing the Model object.
        return self.name
    
# Model Representing a book 
class Book(models.Model):
    title = models.CharField(max_length=200)
    
    # ForeignKey used because book can only have one author, but authors can have multiple books.
    # 'Author' in strings because the class Author has not been made. *Class Author is below the book*
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn" target=_blank>ISBN number</a>')
    book_added = models.DateField(null=True, blank=True, help_text='Book added into the system.')
    
    # many to Many field used because genre can contain many books. Books can cover many genres.
    # Because Genre has been defined so we can specify the object obove.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book.')
    language = models.ForeignKey('BookLanguage', on_delete=models.SET_NULL, null=True)
    
    # Create a string for the Genre. This is required to display genre in Admin Panel
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'
    
    def __str__(self):
        # String for representing the model object
        return self.title.title()
    
    def get_absolute_url(self):
        # Returns the URL to access a detail record for this book.
        return reverse('book-detail', args=[str(self.id)])
    
# Model representing a book's Language 
class BookLanguage(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the book's natural language (e.g. English, German, Spanish, etc.)")
    
    def __str__(self):
        return self.name


# BookInstance represents a specific copy of a book that someone might borrow
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across the whole library')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)    
    # book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, blank=True, null=True)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book Availability'
    )
    
    @property
    def is_overdue(self):
        """Determines if the book is over due based on due date and current date"""
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back', 'status']
        permissions = (("can_mark_returned", "Set book as returned"),)
        
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    


# Model representing an author
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    # Calculates the authors age.   
    @property
    def author_age(self):
        today = date.today()
        try: 
            birthday = self.date_of_birth.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.date_of_birth.replace(year=today.year, month=self.date_of_birth.month+1, day=1)
        if birthday > today:
            return today.year - self.date_of_birth.year - 1
        else:
            return today.year - self.date_of_birth.year

    
        
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
