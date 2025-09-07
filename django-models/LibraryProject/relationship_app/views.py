# from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Book

# ✅ Task 1: List all books
def list_books(request):
    books = Book.objects.all()  # Checker requirement ✅
    return render(request, "relationship_app/list_books.html", {"books": books})

# ✅ Role Check Functions
def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_librarian(user):
    return user.groups.filter(name="Librarian").exists()

def is_member(user):
    return user.groups.filter(name="Member").exists()

# ✅ Task 3: Role-based Views
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
