from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Comment, Post
from taggit.models import Tag
from taggit.forms import TagWidget

# Registration form with email
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# User update form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Write your comment..."}),
        max_length=2000,
        help_text="2000 characters max."
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        c = self.cleaned_data.get('content','').strip()
        if not c:
            raise forms.ValidationError("Comment cannot be empty.")
        return c


# Profile update form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class PostForm(forms.ModelForm):
    # tags will be presented as a simple input where users can add comma-separated tags
    tags = forms.CharField(required=False, help_text="Comma-separated tags", widget=forms.TextInput())

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),  
        }

    def clean_tags(self):
        # normalize tags: split by commas, strip whitespace, remove empties
        raw = self.cleaned_data.get('tags', '')
        if not raw:
            return ''
        tags = [t.strip() for t in raw.split(',') if t.strip()]
        return ','.join(tags)

    def save(self, commit=True):
        # override to handle taggit
        tags_raw = self.cleaned_data.pop('tags', '')
        instance = super().save(commit=commit)
        if tags_raw is not None:
            tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
            # set tags replacing existing
            instance.tags.set(*tags)
        return instance