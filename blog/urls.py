#this urls.py file connects the views and templates together in the website.

from django.urls import path
from .views import home,about, like_post, favorite_post, post_favorite_list
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView
)



app_name = "blog"
urlpatterns = [
	# path('home/',home, name="blog-home"),  # this is for functional based views
	path('home/', PostListView.as_view(), name="blog-home"), #this is for class based views
	path('', PostListView.as_view(), name="blog-home"),
	path('home/user/<str:username>/', UserPostListView.as_view(), name="user-posts"),
	path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
	path('post/<int:pk>/favorite_post/', favorite_post, name="favorite_post"),
	path('post/new/', PostCreateView.as_view(), name="post-create"),
	path('about/',about, name="blog-about"),
	path('like/',like_post, name="like_post"),
	path('favorites', post_favorite_list, name='post_favorite_list'),

]