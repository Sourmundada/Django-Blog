from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    followers = models.ManyToManyField(User, related_name='category_follower')

    def __str__(self):
        return self.name

    def total_followers(self):
        return self.followers.count()

class Post(models.Model):

    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    content = RichTextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='draft')
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    views = models.IntegerField(default=0, blank=True, null=True)
    author_profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()

    # def feed_posts(self):
    #     return self.

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # many to one relation = Foreign Key
    # Related names can be used while accessing the querysets.
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.content}'

class Profile(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    bio = models.TextField()
    followers = models.ManyToManyField(User, related_name='author_follower')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.author.username

    def total_followers(self):
        return self.followers.count()