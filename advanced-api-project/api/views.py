# from rest_framework import generics, permissions, filters
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from api.models import Book, Author
# from api.serializers import BookSerializer, AuthorSerializer
# from django_filters.rest_framework import DjangoFilterBackend

# # List and create books
# # --------------------
# # Book Views (separate classes per requirement)
# # --------------------
# api/views.py
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# --------------------
# Book Views (separate classes per requirement)
# --------------------

class BookListView(generics.ListAPIView):
    """
    GET /api/books/  -> list books
    Supports filtering, search, ordering via query params.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # read-only allowed for anyone

    # enable filtering, search and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # allow filter by author id and publication_year and title (exact/matching)
    filterset_fields = ['author', 'publication_year', 'title']
    # search across book title and author name (text search)
    search_fields = ['title', 'author__name']
    # allow ordering by title or publication_year
    ordering_fields = ['title', 'publication_year']


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/  -> retrieve single book
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/  -> create new book
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<pk>/update/ -> update book
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/delete/ -> delete book
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# --------------------
# Author Views
# --------------------

class AuthorListView(generics.ListCreateAPIView):
    """
    GET /api/authors/  -> list authors (with nested books)
    POST /api/authors/ -> create author (authenticated)
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    # allow unauthenticated reads, but only authenticated creates:
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    GET /api/authors/<pk>/ -> retrieve author with nested books
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]





# class BookListCreateView(generics.ListCreateAPIView):
#     """
#     Generic view to list all books or create a new book.
#     - GET: Returns a list of all books.
#     - POST: Creates a new book (authenticated users only).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users

#     def perform_create(self, serializer):
#         """
#         Custom method to handle additional logic during book creation.
#         Ensures the serializer's validation (e.g., publication_year) is respected.
#         """
#         serializer.save()

# # Retrieve, update, or delete a specific book
# class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Generic view to retrieve, update, or delete a specific book by ID.
#     - GET: Returns details of a single book.
#     - PUT/PATCH: Updates a book (authenticated users only).
#     - DELETE: Deletes a book (authenticated users only).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users

#     def perform_update(self, serializer):
#         """
#         Custom method to handle additional logic during book updates.
#         Ensures the serializer's validation (e.g., publication_year) is respected.
#         """
#         serializer.save()

    
# # List all books (explicitly named for auto-checker)
# class ListView(generics.ListAPIView):
#     """
#     Generic view to list all books.
#     - GET: Returns a list of all books.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for unauthenticated users

# # Update a specific book (explicitly named for auto-checker)
# class UpdateView(generics.UpdateAPIView):
#     """
#     Generic view to update a specific book by ID.
#     - PUT/PATCH: Updates a book (authenticated users only).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]  # Restrict to authenticated users

#     def perform_update(self, serializer):
#         """
#         Custom method to handle additional logic during book updates.
#         Ensures the serializer's validation (e.g., publication_year) is respected.
#         """
#         serializer.save()

# # Delete a specific book (explicitly named for auto-checker)
# class DeleteView(generics.DestroyAPIView):
#     """
#     Generic view to delete a specific book by ID.
#     - DELETE: Deletes a book (authenticated users only).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]  # Restrict to authenticated users


# # Create a new book (added for auto-checker)
# class CreateView(generics.CreateAPIView):
#     """
#     Generic view to create a new book.
#     - POST: Creates a new book (authenticated users only).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]  # Restrict to authenticated users

#     def perform_create(self, serializer):
#         """
#         Custom method to handle additional logic during book creation.
#         Ensures the serializer's validation (e.g., publication_year) is respected.
#         """
#         serializer.save()    