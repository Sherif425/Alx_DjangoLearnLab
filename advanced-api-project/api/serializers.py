from rest_framework import serializers
from .models import Book, Author
from datetime import datetime


# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model.
    - Validates publication_year is not in the future.
    - Includes author as a PK (default ModelSerializer behavior).
    """
    class Meta:
        model=Book
        fields= ['id', 'title', 'publication_year', 'author']  # Serialize all fields of Book


    def validate_publication_year(self, year):
        current_year = datetime.now().year
        if year > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return year
    
# Serializer for the Author model with nested Book serialization
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author model and nests related books.
    - books: uses BookSerializer(many=True, read_only=True) to list an author's books.
      This is a read-only nested representation — simple and avoids dealing with writable nested logic.
    """
    books = BookSerializer(many=True, read_only=True) # Nested serializer for related books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include name and related books

