from django.contrib import admin
from .models import Book



class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')

    # Enable search by title and author
    search_fields = ('title', 'author')

    # Add filter for publication year
    list_filter = ('publication_year',)
    
    
# Register your models here.
admin.site.register(Book, BookAdmin)