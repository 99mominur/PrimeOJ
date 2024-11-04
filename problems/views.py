from django.shortcuts import render, redirect
from .models import Problem, TestCase
from  .forms import ProblemForm, TestCaseForm
# Create your views here.

def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_testcase')
    else:
        form = ProblemForm()
    return render(request, 'problems/create_problem.html', {'form': form})

def create_testcase(request):
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TestCaseForm()
    return render(request, 'problems/create_testcase.html', {'form': form})

def problem_details(request, pk):
    problem = Problem.objects.get(pk=pk)
    return render(request, "problems/problem_detail.html", {"problem":problem})