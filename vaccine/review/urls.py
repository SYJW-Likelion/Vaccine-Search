# from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('detail/<str:id>', detail, name = "detail"),
    path('new/', new, name="new"),
    path('edit/<str:id>', edit, name = "edit"),
    path('delete/<str:id>', delete, name ="delete"),
    path('reviewhome/', reviewhome, name = "reviewhome"),
]