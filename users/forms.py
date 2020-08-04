#this forms.py is used for making forms in the django instead of in html and fields means that which field we want to show in the form and model measn which model i want to load in my forms.

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.models import Profile



class UserRegisterForm(UserCreationForm):
	CHOICES = [('M','Male'),('F','Female')]
	YEARS= [x for x in range(1940,2021)]
	email  = forms.EmailField(required=True, help_text='*Required. Please enter a valid email address.*',widget=forms.TextInput(attrs={'placeholder': 'myexample@gmail.com'}))
	gender = forms.ChoiceField(choices=CHOICES, label='Gender', widget=forms.RadioSelect)
	birth_date= forms.DateField(label='Birthday', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))



	class Meta:
		model = User
		fields = ['username', 'email', 'gender','birth_date', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		# fields = ['gender', 'birth_date', 'image']
		fields = ['image']


