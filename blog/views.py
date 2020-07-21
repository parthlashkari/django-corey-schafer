from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
		ListView,
		DetailView,
		CreateView,
		UpdateView,
		DeleteView,
)
from .models import Post
from django.urls import reverse_lazy

#Create your views here.
#This was dummy data that we had created to show data on the website.
# posts = [
# 	{
# 	'author':'Parth Lashkari',
# 	'title':'Blog Post 1',
# 	'content':'First Post Content',
# 	'date_posted':'July-2019-13'
# 	},
# 	{
# 	'author':'Yatharth Lashkari',
# 	'title':'Blog Post 2',
# 	'content':'Second Post Content',
# 	'date_posted':'July-2019-14'
# 	}
# ]
# These are fucntional based views
def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request,"blog/home.html",context)

# These are custom class based views
class PostListView(ListView):
	model 				= Post
	template_name 		= 'blog/home.html' #(if we dont write this here then django will look into the default template with naming convention like this <app>/<model>_<viewtype>.html which we have to create manually other than our home.html page so always try to write 'template_name' when using class based views when not using conventional template.)
	context_object_name = 'posts' #(this is the customised name of object that we are using from above home functional based view but by default class based views use the name of object as object itself that we can see in post_detail.html templates in blog app.)
	ordering 			= ['-date_posted']
	paginate_by	= 5

class UserPostListView(ListView):
	model 				= Post
	template_name 		= 'blog/user_posts.html' 
	context_object_name = 'posts' 
	#ordering 			= ['-date_posted'] # we dont need it coz we r overriding it in get_query_set function below.
	paginate_by	= 5

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')

# now we are creating the conventional class based view
class PostDetailView(DetailView):
	model = Post
	# now we r not using template_name in it instead of it we r created conventional template named <app>/<model>_<viewtype>.html or in this case blog/post_detail.html so we r going to create this template in our blog templates 

class PostCreateView(LoginRequiredMixin, CreateView):
	model  = Post
	fields = ['title', 'content']
	success_url = reverse_lazy('blog:blog-home') #it is useful when after creating new post u want to redirect to the blog-home page otherwise in models.py get_absolute_url will make u redirect to the post_detail.html page or post-detail page and if u define both then success-url will dominate the get-absolute_url

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model  = Post
	fields = ['title', 'content']
	success_url = reverse_lazy('blog:blog-home') 

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = reverse_lazy('blog:blog-home')

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render(request,"blog/about.html",{'title':'About'})