from django.urls import path

from .views import *


app_name = 'theory'

urlpatterns = [
    path('hash/', theory_hash, name='hash')
]
