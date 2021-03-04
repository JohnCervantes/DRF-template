from django.urls import path
from .views import *

urlpatterns = [
    path('hello-view/',  HelloAPIView.as_view()),
    path('users/',  UserProfileAPIView.as_view()),
    path('users/<str:id>',  UserProfileAPIView.as_view())
]
