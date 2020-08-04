from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .validators import validate_file_size

# Create your models here.

#this models.py file means realtional table or schema in the databse and title, content etc are fields in the database table just like in sql. 

class Post(models.Model):
	title 		= models.CharField(max_length = 120)
	content 	= models.TextField()
	date_posted = models.DateTimeField(default = timezone.now) #this will show on which date the post was created.
	author 		= models.ForeignKey(User, on_delete=models.CASCADE) #this means if user got deleted then the authr will get deleted but not vice versa.
	image 		= models.ImageField( default="default1.jpg", upload_to = "profile_pics", blank =True,null =True) #and this allow images to get uploaded in the post and upload_to means in which folder all the files have been saved. 
	likes 		= models.ManyToManyField(User, related_name='likes', blank=True) #it means that one post can have many likes and many posts can have many likes 
	video		= models.FileField(upload_to='profile_vids', blank=True, null=True, validators=[validate_file_size]) # this is used for uploading video or documents likep pdf in the post.
	restrict_comments = models.BooleanField(default=False) #this means that we want posts to allow comments on it or not.
	favorite 	= models.ManyToManyField(User, related_name="favorite", blank=True) #same as likes

	def __str__(self):
		return self.title

	def total_likes(self):
		return self.likes.count()

	#this function means in post-detail template where we want our users to redirect after clicking on post's title in the website.
	def get_absolute_url(self):
		return reverse('blog:post-detail', kwargs={'pk' : self.pk})

	

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE) #this means that if post is deleted then all comments will get deleted also but if comments got deleted then post wil not get deleted obviously. 
	user = models.ForeignKey(User, on_delete=models.CASCADE) # same as above if user got deleted then all comments will get deleted but not vive versa. 
	comment = models.TextField(max_length=160)
	reply = models.ForeignKey('Comment', null = True, related_name='replies', on_delete=models.CASCADE,blank =True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.post.title, str(self.user.username))