#this token file is used for sending confirmation mail to the newly registered user and making the account active after confirmation.

from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
from six import text_type

# class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
# 	def _make_hash_value(self, user, timestamp):
# 		return (
# 		    six.text_type(user.pk) + six.text_type(timestamp) +
# 		    six.text_type(user.profile.email_confirmed)
# 		)

# account_activation_token = AccountActivationTokenGenerator()

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			text_type(user.pk) + text_type(timestamp) +
			text_type(user.profile.email_confirmed)
		)

account_activation_token = AccountActivationTokenGenerator()