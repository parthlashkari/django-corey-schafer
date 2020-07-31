from django.urls import path
from .views import profile,SignUpView, ActivateAccount





app_name = "users"
urlpatterns = [
    # path('register/',register, name = "register-page" ), #for using this first import register in from .views
    path('register/', SignUpView.as_view(), name='register-page'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('profile/',profile, name = "profile-page" ),
]
