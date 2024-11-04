from django.urls import path
from .views import create_contest, contest_list, contest_detail

urlpatterns = [
    path('create/', create_contest, name="create_contest"),
    path("list/", contest_list, name="contest_list"),
    path("details/<int:pk>", contest_detail, name="contest_details"),
]
