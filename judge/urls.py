from django.urls import path
from home.views import home
urlspatterns = [
    path('', home, name='home'),
]