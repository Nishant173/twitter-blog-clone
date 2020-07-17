from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from account.models import Account
from blog.models import Post
from .models import Follower


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request=request, message=f"{username} may now login!")
            return redirect(to='login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request=request, template_name='users/register.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(data=request.POST,
                                         instance=request.user.profile,
                                         files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request=request, message="Your account has been updated!")
        elif not user_form.is_valid() and profile_form.is_valid():
            messages.warning(request=request, message="User data is invalid OR username is already taken")
        elif user_form.is_valid() and not profile_form.is_valid():
            messages.warning(request=request, message="Profile data is INVALID")
        else:
            messages.warning(request=request, message="Both User and Profile data is INVALID")
        
        return redirect(to='profile')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request=request, template_name='users/profile.html', context=context)


@login_required
def follow_info(request, username):
    visitor = get_object_or_404(klass=Account, username=request.user.username)
    user = get_object_or_404(klass=Account, username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(object_list=posts, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers_list = user.followers.all()
    following_list = user.following.all()
    followers_count = len(followers_list)
    following_count = len(following_list)

    visitor_follows_user = visitor.following.filter(following=user).first()
    user_follows_visitor = user.following.filter(following=visitor).first()

    is_following = False # Does visitor follow user?
    is_followed_by = False # Does user follow visitor?
    visiting_own_profile = False

    if visitor_follows_user:
        is_following = True
    if user_follows_visitor:
        is_followed_by = True
    if visitor == user:
        visiting_own_profile = True
    
    context = {
        'visitor': visitor,
        'username': user,
        'visiting_own_profile': visiting_own_profile,
        'posts': posts,
        'followers_list': followers_list,
        'following_list': following_list,
        'followers_count': followers_count,
        'following_count': following_count,
        'page_obj': page_obj,
        'is_following': is_following,
        'is_followed_by': is_followed_by,
    }
    return render(request=request, template_name='users/follow_info.html', context=context)


@login_required
def follow_toggle(request, username):
    """ Toggle the follow button and redirect to same page """
    visitor = get_object_or_404(klass=Account, username=request.user.username)
    user = get_object_or_404(klass=Account, username=username) # User visited
    visitor_follows_user = visitor.following.filter(following=user).first()

    if visitor_follows_user:
        visitor.following.filter(following=user).delete()
        messages.success(request=request, message=f"You unfollowed {user.username}")
    else:
        obj = Follower.objects.create(follower=visitor, following=user)
        obj.save()
        messages.success(request=request, message=f"You successfully followed {user.username}")
    return HttpResponseRedirect(redirect_to=request.META.get('HTTP_REFERER'))