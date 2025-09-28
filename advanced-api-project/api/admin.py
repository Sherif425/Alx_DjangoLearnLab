from django.contrib import admin
from api.models import Author, Book

# Register Author and Book models to make them accessible in the Django admin interface
admin.site.register(Author)
admin.site.register(Book)