from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from django.urls import reverse_lazy
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages     #messages ke types = (messages.debug, message.success, messages.info, message.warning, messages.error)
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activation_token


# Create your views here.
# def register(request):
# 	if request.method == 'POST':
# 		#form = UserCreationForm(request.POST)
# 		form = UserRegisterForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			# we were using these below 2 lines when we hadn't created the login page. 
# 			# messages.success(request, f'Account created for {username}!')
# 			# return redirect('blog:blog-home')
# 			messages.success(request, f'Your account has been created! You are now able to login.')
# 			return redirect('login-page')
# 	else:
# 		#form = UserCreationForm()
# 		form = UserRegisterForm()
# 	return render(request, "users/register.html", {'form': form})


# Sign Up View
class SignUpView(View):
	form_class = UserRegisterForm
	template_name = 'users/register.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			user = form.save(commit=False)
			user.is_active = False # Deactivate account till it is confirmed
			user.save()

			current_site = get_current_site(request)
			subject = 'Activate Your ParthBook Account'
			message = render_to_string('users/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)

			messages.info(request, ('Please Confirm your email to complete registration. A confirmation link has been sent at your provided email address.'))

			return redirect('login-page')

		return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

	def get(self, request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend', *args, **kwargs):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.profile.email_confirmed = True
			user.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, ('Your account has been confirmed.'))
			return redirect('blog:blog-home')
		else:
			messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
			return redirect('blog:blog-home')

@login_required#(redirect_field_name='users/profile')
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
								   request.FILES,
								   instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated successfully!')
			return redirect('users:profile-page')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context =  {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile.html',context)




