from django.shortcuts import render, redirect
from .forms import LoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from core.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .decorators import *
from django.http import HttpResponseRedirect


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.warning(
                request, 'Username or password wrong')

    return render(request, 'user/login.html', {
        'title': 'Login',
    })


def logout_user(request):
    logout(request)
    return render(request, 'user/logout.html', {
        'title': 'Logout'
    })


@login_required(login_url='login')
def profile(request):
    posts = Post.objects.filter(author=request.user)
    post_list = Post.objects.filter(author=request.user)
    comments = Comment.objects.filter(translations__active=False)
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_page)


    # Close and Open a bid
    if request.POST.get('activate'):
        cId = request.POST.get('comment_id')
        comments = Comment.objects.get(id=cId)
        
        if comments.active == True:
            comments.active = False
            messages.success(request, 'Comment hidden')
            comments.save()

        elif comments.active == False:
            comments.active = True
            messages.success(request, 'Comment accepted')
            comments.save()
        
        return redirect('profile')






    return render(request, 'user/profile.html', {
        'title': 'Personal profile',
        'posts': posts,
        'comments': comments,
        'page': page,
        'post_list': post_list,
    })


@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Personal profile updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Personal profile update',
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'user/profile_update.html', context)



def comment_del(request, pk):

    Comment.objects.get(id=pk).delete()
    messages.success(request, 'Comment deleted')


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

