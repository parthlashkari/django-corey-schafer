from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .validators import validate_file_size

# Create your models here.

class Post(models.Model):
	title 		= models.CharField(max_length = 120)
	content 	= models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	author 		= models.ForeignKey(User, on_delete=models.CASCADE) 
	image 		= models.ImageField( default="default1.jpg", upload_to = "profile_pics", blank =True,null =True)
	likes 		= models.ManyToManyField(User, related_name='likes', blank=True)
	video		= models.FileField(upload_to='profile_vids', blank=True, null=True, validators=[validate_file_size])
	restrict_comments = models.BooleanField(default=False)
	favorite 	= models.ManyToManyField(User, related_name="favorite", blank=True)

	def __str__(self):
		return self.title

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse('blog:post-detail', kwargs={'pk' : self.pk})

	

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField(max_length=160)
	reply = models.ForeignKey('Comment', null = True, related_name='replies', on_delete=models.CASCADE,blank =True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.post.title, str(self.user.username))