from django.urls import path
from account.views import *

urlpatterns=[
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('error/', signup, name="signup"),
]