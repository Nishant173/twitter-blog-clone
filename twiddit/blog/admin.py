from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date_posted', 'author')
    list_filter = ('date_posted', )
    search_fields = ['author', 'title', 'content']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'date_posted')
    list_filter = ('date_posted', )
    search_fields = ['post', 'author', 'content']


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)