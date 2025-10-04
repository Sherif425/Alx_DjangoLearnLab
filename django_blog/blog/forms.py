from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Comment

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

