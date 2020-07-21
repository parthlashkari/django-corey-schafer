from django.urls import path
from .views import register,profile





app_name = "users"
urlpatterns = [
    path('register/',register, name = "register-page" ),
    path('profile/',profile, name = "profile-page" ),
]
