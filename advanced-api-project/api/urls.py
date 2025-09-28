from django.urls import path
from api.views import BookListCreateView, BookDetailView, ListView, UpdateView, DeleteView

# URL patterns for the Book API endpoints
urlpatterns = [
    # Original endpoints for compatibility
    path('books/', BookListCreateView.as_view(), name='book-list-create'),  # List and create books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve, update, delete a book
    
    # New endpoints for auto-checker
    path('books/list/', ListView.as_view(), name='book-list'),  # List all books
    path('books/update/<int:pk>/', UpdateView.as_view(), name='book-update'),  # Update a book
    path('books/delete/<int:pk>/', DeleteView.as_view(), name='book-delete'),  # Delete a book
]