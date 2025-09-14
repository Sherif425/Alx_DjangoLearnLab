from django.contrib import admin
from .models import Book, CustomUser

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "date_of_birth", "is_staff", "is_active"]

class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')

    # Enable search by title and author
    search_fields = ('title', 'author')

    # Add filter for publication year
    list_filter = ('publication_year',)
    
    
# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
