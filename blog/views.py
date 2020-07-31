from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
		ListView,
		DetailView,
		CreateView,
		UpdateView,
		DeleteView,
)
from .models import Post, Comment
from .forms import CommentModelForm
from django.urls import reverse_lazy
# from django.core.exceptions import ValidationError
# from django import forms

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
class PostListView(LoginRequiredMixin, ListView):
	model 				= Post
	template_name 		= 'blog/home.html' #(if we dont write this here then django will look into the default template with naming convention like this <app>/<model>_<viewtype>.html which we have to create manually other than our home.html page so always try to write 'template_name' when using class based views when not using conventional template.)
	context_object_name = 'posts' #(this is the customised name of object that we are using from above home functional based view but by default class based views use the name of object as object itself that we can see in post_detail.html templates in blog app.)
	ordering 			= ['-date_posted']
	paginate_by	= 5

class UserPostListView(LoginRequiredMixin, ListView):
	model 				= Post
	template_name 		= 'blog/user_posts.html' 
	context_object_name = 'posts' 
	#ordering 			= ['-date_posted'] # we dont need it coz we r overriding it in get_query_set function below.
	paginate_by	= 5

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')

# now we are creating the conventional class based view
class PostDetailView(LoginRequiredMixin, DetailView):
	model = Post
	fields = ['title', 'content','video', 'image']
	form_class = CommentModelForm
	
	# now we r not using template_name in it instead of it we r created conventional template named <app>/<model>_<viewtype>.html or in this case blog/post_detail.html so we r going to create this template in our blog templates 
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		is_liked = False
		is_favorite = False
		if self.object.likes.filter(id = self.request.user.id).exists():
			is_liked = True

		if self.object.favorite.filter(id = self.request.user.id).exists():
			is_favorite = True

		context['comments'] = Comment.objects.filter(post=self.object,reply=None).order_by('-timestamp')[:1000]
		context['form'] = CommentModelForm()
		context['comment_form'] = CommentModelForm()
		context['is_liked'] = is_liked
		context['is_favorite'] = is_favorite
		context['post'] = self.request.user
		context['total_likes'] = self.object.total_likes()

		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		

		# post = get_object_or_404(Post)
		# form = self.get_form()
		# if form.is_valid():
		#     return self.form_valid(form)
		# else:
		#     return self.form_invalid(form)
		if request.method == "POST":
			comment_form = CommentModelForm(request.POST or None)
			if comment_form.is_valid():
				comment = request.POST.get('comment')
				reply_id = request.POST.get('comment_id')
				comment_qs = None
				if reply_id:
					comment_qs = Comment.objects.get(id = reply_id)
				comments = Comment.objects.create(post=self.object, user =request.user, comment=comment, reply=comment_qs)
				comments.save()
				#success_url = reverse_lazy(post.get_absolute_url())

				return redirect(self.object.get_absolute_url())
		else:
			comment_form = CommentModelForm()

	def form_valid(self, form):
		form.instance.article = self.object
		# form.save()
		return super().form_valid(form)
	# if request.method == "POST":
	# 	comment_form = CommentModelForm(request.POST or None)
	# 	if comment_form.is_valid():
	# 		comment = request.POST.get('comment')
	# 	else:
	# 		comment_form = CommentModelForm()

def like_post(request):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False
	else:
		post.likes.add(request.user)
		is_liked = True
	return redirect(post.get_absolute_url())

def post_favorite_list(request):
	user = request.user
	favorite_posts = user.favorite.all()
	context = {
		'favorite_posts':favorite_posts,
	}
	return render(request, 'blog/post_favorite_list.html', context)

def favorite_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if post.favorite.filter(id=request.user.id).exists():
		post.favorite.remove(request.user)
		is_liked = False
	else:
		post.favorite.add(request.user)
	return redirect(post.get_absolute_url())


class PostCreateView(LoginRequiredMixin, CreateView):
	model  = Post
	fields = ['title', 'content','video', 'image', 'restrict_comments']
	success_url = reverse_lazy('blog:blog-home') #it is useful when after creating new post u want to redirect to the blog-home page otherwise in models.py get_absolute_url will make u redirect to the post_detail.html page or post-detail page and if u define both then success-url will dominate the get-absolute_url

	def form_valid(self, form):
		form.instance.author = self.request.user
		# image = form.cleaned_data.get('image')
		# video = form.cleaned_data.get('video')
		# if form.instance.image and form.instance.video:
		# 	# messages.error(self.request, f'no')
		# 	raise forms.ValidationError("u cant post ")
		# 	return redirect('blog:post-create')
		# form.save()
		messages.success(self.request, f'Your new post has been successfully created')
		return super().form_valid(form)
	def form_invalid(self, form):
		messages.warning(self.request, f'Please correct the error below')
		return super().form_invalid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model  = Post
	fields = ['title', 'content', 'video', 'image', 'restrict_comments']
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


