from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', ) # 'post' and 'author' should not be in this form


class SearchForm(forms.Form):
    search_string = forms.CharField(max_length=200)