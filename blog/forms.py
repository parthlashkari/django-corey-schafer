from django import forms
from .models import Post, Comment
from users.models import Profile
from django.contrib.auth.models import User



class CommentModelForm(forms.ModelForm):
	comment = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment here!', 'rows': '3', 'cols': '50'}))
	class Meta:
		model = Comment
		fields = ['comment']