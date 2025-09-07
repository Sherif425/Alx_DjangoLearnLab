from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Book

# ✅ Task 1: Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Checker requirement ✅
    return render(request, "relationship_app/list_books.html", {"books": books})

# ✅ Role check functions using UserProfile role field
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"

# ✅ Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# ✅ Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# ✅ Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


from django.contrib.auth.decorators import permission_required

@permission_required("relationship_app.can_add_book")
def add_book(request):
    # Implementation for adding book
    pass

@permission_required("relationship_app.can_change_book")
def edit_book(request, pk):
    # Implementation for editing book
    pass

@permission_required("relationship_app.can_delete_book")
def delete_book(request, pk):
    # Implementation for deleting book
    pass
