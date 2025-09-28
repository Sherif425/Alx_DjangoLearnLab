from .api.models import Author, Book
from .api.serializers import AuthorSerializer, BookSerializer
from datetime import datetime

# Create an author
author = Author.objects.create(name="J.K. Rowling")

# Create books
book1 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", publication_year=1997, author=author)
book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=author)

# Serialize the author with nested books
serializer = AuthorSerializer(author)
print(serializer.data)

# Test book serializer with valid data
book_data = {'title': 'Test Book', 'publication_year': 2020, 'author': author.id}
book_serializer = BookSerializer(data=book_data)
if book_serializer.is_valid():
    book_serializer.save()
    print(book_serializer.data)

# Test book serializer with invalid publication year
invalid_book_data = {'title': 'Future Book', 'publication_year': datetime.now().year + 1, 'author': author.id}
invalid_serializer = BookSerializer(data=invalid_book_data)
try:
    invalid_serializer.is_valid(raise_exception=True)
except Exception as e:
    print(e)  # Should print validation error for future year