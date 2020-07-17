import django_filters
from .models import Post

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ('title', 'content')