from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# from django.utils import simplejson
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from .filters import SearchFilter
from .forms import CommentForm, SearchForm
from .models import Post, Comment
from account.models import Account


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html' # Format: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        """ Shows user's posts only if you're following them """
        user_account = Account.objects.filter(username=self.request.user).first()
        following_list = [following.get_following for following in user_account.following.all()]
        following_list.append(user_account) # Show posts of current user as well
        post_context = Post.objects.filter(author__in=following_list).order_by('-date_posted')
        # if 'search' not in self.request.GET:
        #     search_term = str(self.request.GET['search']).strip()
        #     user_search_tag = 'u/'
        #     user_search_tag_length = len(user_search_tag)
        #     if search_term[:user_search_tag_length] == user_search_tag:
        #         user_searched = search_term[user_search_tag_length:].replace(' ', '')
        #         user_searched = Account.objects.filter(username=user_searched).first()
        #         post_context = Post.objects.filter(author__in=[user_searched]).order_by('-date_posted')
        #     else:
        #         post_context = post_context.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))
        return post_context


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html' # Format: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(klass=Account, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


@login_required
def post_detail(request, slug, *args, **kwargs):
    post = get_object_or_404(klass=Post, slug=slug, *args, **kwargs)
    comments = post.comments.order_by('date_posted')
    new_comment = None
    
    is_upvoted, is_downvoted = False, False
    if post.upvotes.filter(id=request.user.id).exists():
        is_upvoted = True
    if post.downvotes.filter(id=request.user.id).exists():
        is_downvoted = True

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request=request, message='Successfully posted the comment!')
        else:
            messages.warning(request=request, message='Could not post the comment!')
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'is_upvoted': is_upvoted,
        'is_downvoted': is_downvoted,
        'net_votes': post.total_upvotes - post.total_downvotes,
        'total_upvotes': post.total_upvotes,
        'total_downvotes': post.total_downvotes,
    }
    return render(request=request, template_name='blog/post_detail.html', context=context)


@login_required
def upvote_post(request, *args, **kwargs):
    post = get_object_or_404(klass=Post, id=request.POST.get('post_id'), *args, **kwargs)
    is_upvoted = False
    is_downvoted = False
    if post.upvotes.filter(id=request.user.id).exists():
        post.upvotes.remove(request.user)
        is_upvoted = False
    else:
        post.upvotes.add(request.user)
        is_upvoted = True
    return HttpResponseRedirect(redirect_to=post.get_absolute_url())


@login_required
def downvote_post(request, *args, **kwargs):
    post = get_object_or_404(klass=Post, id=request.POST.get('post_id'), *args, **kwargs)
    is_downvoted = False
    is_upvoted = False
    if post.downvotes.filter(id=request.user.id).exists():
        post.downvotes.remove(request.user)
        is_downvoted = False
    else:
        post.downvotes.add(request.user)
        is_downvoted = True
    return HttpResponseRedirect(redirect_to=post.get_absolute_url())


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/' # Redirects to home page on the successful deletion of the post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form=form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/' # Redirects to home page on the successful deletion of the post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form=form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # Redirects to home page on the successful deletion of the post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    context = {'title': 'About'}
    return render(request=request, template_name='blog/about.html', context=context)