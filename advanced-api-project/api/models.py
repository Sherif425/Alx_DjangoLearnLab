from django.db import models

# Author model to store author information
class Author(models.Model):
    name = models.CharField(max_length=50)  # Stores the author's name, max length 100 characters

    def __str__(self):
        return self.name


# Book model to store book information with a relationship to Author
class Book(models.Model):
    title = models.CharField(max_length=50)  # Stores the book's title, max length 200 characters
    publication_year = models.IntegerField()   # Stores the year the book was published

    Author= models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, # Deletes books if the associated author is deleted
        related_name="books")   # Allows reverse access from Author to related Books

    def __str__(self):
        return self.title