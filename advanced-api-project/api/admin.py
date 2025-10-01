from django.contrib import admin
from api.models import Author, Book

# # Register Author and Book models to make them accessible in the Django admin interface
# admin.site.register(Author)
# admin.site.register(Book)




@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publication_year')
    list_filter = ('publication_year', )
    search_fields = ('title', 'author__name')
