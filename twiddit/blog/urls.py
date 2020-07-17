from django.urls import path
from . import views

urlpatterns = [
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('', views.PostListView.as_view(), name='blog-home'),
    path('home/', views.PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name='blog-about'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('upvote/', views.upvote_post, name='upvote-post'),
    path('downvote/', views.downvote_post, name='downvote-post'),
    # path('?search=<str:query>', views.search_view, name='search-results'),
]