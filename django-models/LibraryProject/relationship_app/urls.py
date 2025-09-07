# from django.urls import path
# from . import views
# from .views import list_books

# urlpatterns = [
#     path("books/", views.list_books, name="list_books"),
#     path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
#     path("register/", views.register_view, name="register"),
#     path("login/", views.login_view, name="login"),
#     path("logout/", views.logout_view, name="logout"),
# ]
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # ✅ Task 1: List of books
    path("books/", views.list_books, name="list_books"),

    # ✅ Task 2: Authentication URLs
    path(
        "login/",
        LoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
]
