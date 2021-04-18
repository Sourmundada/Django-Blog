from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Category, Post, Comment, Profile
from django.views.generic import ListView, CreateView
from .forms import PostForm, CommentForm, SignUpForm, LoginForm, ChangePasswordForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash

class PostListView(ListView):
    queryset = Post.objects.filter(status='publish')
    template_name = 'myapp/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3


# def create_post(request):
#      if request.method == 'GET':
#         return render(request, 'myapp/post_create.html', {'form': PostForm()})
#      else:
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('PostListView')
#         else:
#             return render(request, 'myapp/post_create.html', {'error': 'Invalid Data', 'form': PostForm()})

# class create_post(LoginRequiredMixin, CreateView):
#     form_class = PostForm
#     template_name = 'myapp/post_create.html'
#     success_url = reverse_lazy('PostListView')

def view_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    post_views = Post.objects.get(slug=post_slug)
    post_views.views += 1
    post_views.save()

    liked = False
    disliked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    if post.dislikes.filter(id=request.user.id).exists():
        disliked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'myapp/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'liked': liked, 'disliked': disliked})
    # Unused Variable Error


# @login_required
# def update_post(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     form = PostForm(instance=post)
#     if request.method == 'GET':
#         return render(request, 'myapp/post_update.html', {'form': form})
#     else:
#         update_form = PostForm(request.POST, instance=post)
#         if update_form.is_valid():
#             update_form.save()
#             return redirect('PostListView')
#         else:
#             return render(request, 'myapp/post_update.html', {'form': form, 'error': 'Invalid Information'})


# @login_required
# def delete_post(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('PostListView')


def category_post(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)

    followed = False
    if category.followers.filter(id=request.user.id).exists():
        followed = True

    total_followers = category.followers.count()
    followers = category.followers.all()
    
    return render(request, 'myapp/category.html', {'posts': posts, 'followed': followed, 'total_followers': total_followers, 'category': category, 'followers': followers})


def search_post(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(category__name__icontains=query)
        # You can use icontains lookup on text fields. user is related (integer) field. Instead of user use user__username.
    )
    return render(request, 'myapp/search.html', {'posts': posts})


def CategoryListView(request):
    categories = Category.objects.all()
    return render(request, 'myapp/category_list.html', {'categories': categories})


# class CategoryCreateView(LoginRequiredMixin, CreateView):
#     model = Category
#     template_name = 'myapp/category_create.html'
#     fields = ['name', 'slug']
#     success_url = reverse_lazy('CategoryListView')


# @login_required
# def delete_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     if request.method == 'POST':
#         category.delete()
#         return redirect('CategoryListView')


@login_required
def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    liked = False
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('view_post', args=[str(post_slug)]))


@login_required
def unlike_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    return HttpResponseRedirect(reverse('view_post', args=[str(post_slug)]))


@login_required
def dislike_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    disliked = False
    post.dislikes.add(request.user)
    return HttpResponseRedirect(reverse('view_post', args=[str(post_slug)]))

@login_required
def follow_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    follower = False
    category.followers.add(request.user)
    # If NoReverseMatchError -> Check HTML File
    return HttpResponseRedirect(reverse('category_post', args=[str(category_slug)]))

@login_required
def unfollow_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if category.followers.filter(id=request.user.id).exists():
        category.followers.remove(request.user)
    return HttpResponseRedirect(reverse('category_post', args=[str(category_slug)]))

@login_required
def feed_post(request):
    # my_feed = Category.objects.filter(followers=request.user)
    my_feed = Post.objects.filter(category__followers=request.user)

    # post = Category.objects.filter(name__posts__category)

    posts = my_feed
    return render(request, 'myapp/feed.html', {'posts' : posts}) 

def tagged(request, tag_slug):
    tags = get_object_or_404(Tag, slug=tag_slug)
    # Filter posts by tag name
    posts = Post.objects.filter(tags=tags)

    common_tags = Post.tags.most_common()[:4]

    return render(request, 'myapp/tags.html', {'tags': tags, 'posts' : posts, 'common_tags': common_tags}) 

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html', {'form':SignUpForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('PostListView')
            except IntegrityError:
                return render(request, 'accounts/signup.html', {'form':SignUpForm(), 'error': 'Username is Already Registered, Try Another!'})
        else:
            return render(request, 'accounts/signup.html', {'form':SignUpForm(), 'error': 'Passwords were not same, Try Again!'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'form':LoginForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'accounts/login.html', {'form':LoginForm(), 'error': 'Username or Password is Incorrect'})
        else:
            login(request, user)
            return redirect('PostListView')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('PostListView')


@login_required
def change_password(request):
    if request.method == "POST":
        password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        user = User.objects.get(username__iexact=request.user.username)

        if new_password1 == new_password2:
            success = user.check_password(password)
            if success:
                user.set_password(new_password1)
                user.save()
                return redirect('PostListView')
            else:
                return redirect('change_password')
        else:
            return redirect('change_password')
    
    return render(request, 'accounts/change_password.html')

def author_profile(request, username):

    profile = get_object_or_404(Profile, author__username=username)

    followed = False
    if profile.followers.filter(id=request.user.id).exists():
        followed = True

    posts = Post.objects.filter(author_profile=profile)

    return render(request, 'accounts/profile.html', {'profile': profile, 'posts': posts, 'followed': followed})

@login_required
def follow_author(request, username):
    profile = get_object_or_404(Profile, author__username=username)

    follower = False
    profile.followers.add(request.user)
    # If NoReverseMatchError -> Check HTML File
    return HttpResponseRedirect(reverse('profile', args=[str(username)]))

@login_required
def unfollow_author(request, username):
    profile = get_object_or_404(Profile, author__username=username)
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
    return HttpResponseRedirect(reverse('profile', args=[str(username)]))