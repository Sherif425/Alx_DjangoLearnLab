Advanced API Project - Views Documentation
Overview
This Django project uses Django REST Framework to provide API endpoints for managing Book instances. The views are implemented using DRF's generic views to handle CRUD operations efficiently.
View Configurations

BookListCreateView (api/views.py):

Endpoint: GET /api/books/ (list), POST /api/books/ (create)
Purpose: Lists all books or creates a new book.
Permissions: Read-only for unauthenticated users; full access for authenticated users (IsAuthenticatedOrReadOnly).
Customization: Uses perform_create to ensure serializer validation (e.g., publication_year not in the future).


BookDetailView (api/views.py):

Endpoint: GET /api/books/<int:pk>/ (retrieve), PUT/PATCH /api/books/<int:pk>/ (update), DELETE /api/books/<int:pk>/ (delete)
Purpose: Handles operations on a single book by ID.
Permissions: Read-only for unauthenticated users; full access for authenticated users (IsAuthenticatedOrReadOnly).
Customization: Uses perform_update to ensure serializer validation during updates.



URL Patterns

Defined in api/urls.py and included in the project's urls.py under the /api/ prefix.
/api/books/: Maps to BookListCreateView.
/api/books/<int:pk>/: Maps to BookDetailView.

Testing

Use tools like Postman or curl to test endpoints.
Ensure a superuser exists for authenticated requests (python manage.py createsuperuser).
Test cases include listing books, retrieving a book, creating/updating/deleting books, and verifying permission restrictions.

Custom Settings

Permissions: The IsAuthenticatedOrReadOnly permission class ensures secure access control.
Validation: The BookSerializer (defined in api/serializers.py) enforces that publication_year is not in the future, integrated into the views via perform_create and perform_update.
