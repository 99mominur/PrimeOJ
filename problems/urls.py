from django.urls import path
from .views import create_problem, create_testcase, problem_details


urlpatterns = [
    path('create/', create_problem, name='create_problem'),
    path('create_testcase/', create_testcase, name='create_testcase'),
    path("details/<int:pk>", problem_details, name="problem_details"),
]