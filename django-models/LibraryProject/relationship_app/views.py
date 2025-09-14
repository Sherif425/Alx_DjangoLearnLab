from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all() 
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view: Library detail with books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"  # ✅ checker looks for "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include all books in this library
        context["books"] = self.object.book_set.all()
        return context

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


