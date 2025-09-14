import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def get_books_by_author(author_name):
    books = Book.objects.filter(author__name=author_name)
    return [book.title for book in books]

# 2. List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return [book.title for book in library.books.all()]

# 3. Retrieve the librarian for a library
def get_librarian(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian.name if hasattr(library, "librarian") else "No librarian assigned"

if __name__ == "__main__":
    print(get_books_by_author("J.K. Rowling"))
    print(get_books_in_library("Central Library"))
    print(get_librarian("Central Library"))
