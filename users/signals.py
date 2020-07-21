from django.db.models.signals import post_save #post_save signal indicates that a new user is created
from django.contrib.auth.models import User
from django.dispatch import receiver  #receiver  takes the above signal
from .models import Profile 


@receiver(post_save, sender = User) #this receiver decorator takes 2 arguments 1st post_save which means that a new user is created and sender means for whom the profile is to be created. 
def create_profile(sender, instance, created , **kwargs): #this is a function for receiver in which instance of the User is given
	if created:
		Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()
    




