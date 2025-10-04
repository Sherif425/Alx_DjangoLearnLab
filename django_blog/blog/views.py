from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.decorators import login_required, UserPassesTestMixin
from .models import Post, Comment
from django.contrib.auth.models import User
from .forms import ProfileForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q



# List all posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]


# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CommentForm()
        return ctx


# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Edit an existing post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]
    context_object_name = "post"


# Delete a post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog:post-list")


class ProfileView(ListView):
    model = Post
    template_name = "blog/profile.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = User.objects.get(username=self.kwargs.get("username"))
        return context


@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(View):
    template_name = "blog/profile.html"

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # 👈 this ensures "save()" exists
            return redirect("blog:profile")
        return render(request, self.template_name, {"form": form})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        # store post object for later use
        self.post_obj = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        messages.success(self.request, "Comment posted.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_obj.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to edit this comment.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.get_object().post.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        post_url = self.object.post.get_absolute_url()
        self.object.delete()
        messages.success(request, "Comment deleted.")
        return redirect(post_url)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment_form.html"

    def form_valid(self, form):
        # Attach the logged-in user as author
        form.instance.author = self.request.user
        # Attach the post from pk in URL
        post_obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post_obj
        return super().form_valid(form)

    def get_success_url(self):
        # After adding comment, go back to post detail
        return reverse_lazy("post-detail-pk", kwargs={"pk": self.kwargs["pk"]})


class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        # search title, content, tag names
        qs = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')
        return qs

class TagListView(ListView):
    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return Post.objects.filter(tags__name__iexact=tag).distinct().order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag'] = self.kwargs.get('tag')
        return ctx