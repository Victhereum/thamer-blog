
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from .forms import NewComment, PostCreateForm, CategoryCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .utils import update_views
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt

def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
    context = {
        'title': 'Home',
        'posts': posts,
        'page': page,
    }
    return render(request, 'blog/index.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About me'})

@xframe_options_exempt
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter(translations__active=True)     # if you want to make comment filter change .all() to = .filter(active=True)

    # check before save data from comment form
    if request.method == 'POST':
        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            # Deprecated line to prevent form to post data when refresh a page
            # comment_form = NewComment()
            return redirect('detail', post_id)
    else:
        comment_form = NewComment()

    update_views(request, post)

    context = {
        'title': post,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'blog/detail.html', context)







# List all categories
def categories(request):
    categories = Category.objects.all()

    return render(request, "blog/categories.html", {
        'categories':categories
    })


# Items within the specified category
def category(request, slug=None):
    # Filter all items which belongs to the category
    category = None
    categories = Category.objects.all()

    posts = Post.objects.all()

    

    if slug:
        category = get_object_or_404(Category, slug=slug)
        posts = posts.filter(category=category)


    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)


    context = {
    'categories':categories,
    'category':category,
    'posts':posts,
    'page': page,
    }

    return render(request, "blog/category.html", context)



def search(request):
    q = request.GET.get('q')

    if q:
        posts = Post.objects.filter(Q(translations__title__icontains=q)|Q(content__icontains=q)).order_by('-id')

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)

    return render(request, "blog/search.html", {
        'posts': posts
    })



class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    # fields = ['title', 'content']
    template_name = 'blog/new_category.html'
    form_class = CategoryCreateForm

    success_url = '/'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'blog/new_post.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False