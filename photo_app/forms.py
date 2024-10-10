from django import forms
from .models import User, Post, Comment


class PhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["profile_picture", "sity"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
