from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.views import UserLogoutView, UserRegisterView, UserSuggestionView, UserMeView, PasswordChangeView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', UserLogoutView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('password_change/', PasswordChangeView.as_view()),
    path('me/', UserMeView.as_view()),
    path('suggestions/', UserSuggestionView.as_view()),
]
