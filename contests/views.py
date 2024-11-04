
from django.shortcuts import get_object_or_404, render, redirect
from .models import Contest
from .forms import ContestForm

def create_contest(request):
    if request.method == "POST":
        form = ContestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contest_list')
    else:
        form = ContestForm()
    return render(request, "contests/create_contest.html", {'form':form})


def contest_list(request):
    contests = Contest.objects.all()
    return render(request, 'contests/contest_list.html', {'contests': contests})

def contest_detail(request, pk):
    contest = get_object_or_404(Contest, pk=pk)
    # Handle logic for contest type (public/private/protected)
    # Redirect based on contest type and user's eligibility
    return render(request, 'contests/contest_detail.html', {'contest': contest})
