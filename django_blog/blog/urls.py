from django.urls import path
from . import views_auth, views

app_name = "blog"

urlpatterns = [
    # Blog posts
    path("", views.PostListView.as_view(), name="post-list"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail-pk"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # Auth
    path("login/", views_auth.login_view, name="login"),
    path("logout/", views_auth.logout_view, name="logout"),
    path("register/", views_auth.register, name="register"),

    # Profile
    path("profile/<str:username>/", views.ProfileView.as_view(), name="profile"),
    path("profile/", views.ProfileUpdateView.as_view(), name="profile"),

    # Comments

    path("post/<slug:slug>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/edit/", views.CommentUpdateView.as_view(), name="comment-edit"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path('post/<int:pk>/comments/new/', views.AddCommentView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]


