from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from api.models import Book
from api.serializers import BookSerializer

# List and create books
class BookListCreateView(generics.ListCreateAPIView):
    """
    Generic view to list all books or create a new book.
    - GET: Returns a list of all books.
    - POST: Creates a new book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users

    def perform_create(self, serializer):
        """
        Custom method to handle additional logic during book creation.
        Ensures the serializer's validation (e.g., publication_year) is respected.
        """
        serializer.save()

# Retrieve, update, or delete a specific book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view to retrieve, update, or delete a specific book by ID.
    - GET: Returns details of a single book.
    - PUT/PATCH: Updates a book (authenticated users only).
    - DELETE: Deletes a book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users

    def perform_update(self, serializer):
        """
        Custom method to handle additional logic during book updates.
        Ensures the serializer's validation (e.g., publication_year) is respected.
        """
        serializer.save()