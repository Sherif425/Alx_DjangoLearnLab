# api/models.py
from django.db import models

class Author(models.Model):
    """
    Represents an author. Simple model with a name field.
    The related_name on Book.author is 'books', so for an author instance you can access
    author.books.all() to get all books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book. Fields:
    - title: short title string
    - publication_year: positive integer for the year (we'll validate it in the serializer)
    - author: FK to Author establishing one-to-many (one author → many books)
    """
    title = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    # related_name='books' makes reverse access meaningful: author.books.all()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
