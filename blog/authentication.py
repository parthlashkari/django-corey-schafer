# from django.contrib.auth.models import User

# class EmailAuthbackend(object):
# 	def authenticate(self, Username=None, Password=None):
# 		try:
# 			user = User.objects.get(email=Username)
# 			if user.check_password(Password):
# 				return user
# 			return None
# 		except User.DoesNotExist:
# 			return None
	

# 	def get_user(self, user_id):
# 		try:
# 			return User.objects.get(pk=user_id)
# 		except User.DoesNotExist:
# 			return None

#this file is for authenticating the user from his email id also other than his/her username.
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailAuthbackend(ModelBackend):
    """
    Authentication backend which allows users to authenticate using either their
    username or email address

    Source: https://stackoverflow.com/a/35836674/59984
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # n.b. Django <2.1 does not pass the `request`

        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        # The `username` field is allows to contain `@` characters so
        # technically a given email address could be present in either field,
        # possibly even for different users, so we'll query for all matching
        # records and test each one.
        users = user_model._default_manager.filter(
            Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username)
        )

        # Test whether any matched user has the provided password:
        for user in users:
            if user.check_password(password):
                return user
        if not users:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (see
            # https://code.djangoproject.com/ticket/20760)
            user_model().set_password(password)
