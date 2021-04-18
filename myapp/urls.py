from django.urls import path
from myapp import views

urlpatterns = [
    path('register/', views.signupuser, name='signup'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/<username>/', views.author_profile, name='profile'),
    path('profile/<username>/follow/', views.follow_author, name='follow_author'),
    path('profile/<username>/unfollow/', views.unfollow_author, name='unfollow_author'),
    path('change_password/', views.change_password, name='change_password'),
    path('', views.PostListView.as_view(), name='PostListView'),
    path('search/', views.search_post, name='search_post'),
    # path('create/', views.create_post.as_view(), name='create_post'),
    path('category/', views.CategoryListView, name='CategoryListView'),
    path('tags/<tag_slug>/', views.tagged, name='tags'),
    path('feed/', views.feed_post, name='feed_post'),
    # path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    # path('category/<category_slug>/delete/', views.delete_category, name='delete_category'),
    # path('<post_slug>/update/', views.update_post, name='update_post'),
    # path('<post_slug>/delete/', views.delete_post, name='delete_post'),
    path('category/<category_slug>/', views.category_post, name='category_post'),
    path('like/<post_slug>/', views.like_post, name='like_post'),
    path('follow/<category_slug>/', views.follow_category, name='follow_category'),
    path('unfollow/<category_slug>/', views.unfollow_category, name='unfollow_category'),
    path('dislike/<post_slug>/', views.dislike_post, name='dislike_post'),
    path('unlike/<post_slug>/', views.unlike_post, name='unlike_post'),
    path('p/<post_slug>/', views.view_post, name='view_post'),
]