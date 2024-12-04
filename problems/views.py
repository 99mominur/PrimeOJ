import requests
from django.http import JsonResponse
from django.db.models import Q, Prefetch
from django.shortcuts import render, redirect
from .models import Problem, TestCase, Tag, Solved
from  .forms import ProblemForm, TestCaseForm
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_testcase')
    else:
        form = ProblemForm()
    return render(request, 'problems/create_problem.html', {'form': form})



@login_required(login_url='login')
def problem_list(request):
    from django.db.models import Prefetch, Exists, OuterRef

    # Get search and filter parameters
    search_query = request.GET.get("search", "")
    rating_filter = request.GET.get("rating", None)
    tag_filter = request.GET.getlist("tags")
    solve_status = request.GET.get("status", None)
    sort_by = request.GET.get("sort_by", "title")  # Default sorting by title

    # Solve status filter setup
    solved_subquery = Solved.objects.filter(
        problem=OuterRef('pk'), user=request.user, is_solved=True
    )

    # Base queryset
    problems = Problem.objects.annotate(
        is_solved=Exists(solved_subquery)
    ).prefetch_related(
        Prefetch("tags"),  # Prefetch tags for better performance
    )

    # Apply filters
    if search_query:
        problems = problems.filter(
            Q(title__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()

    if rating_filter:
        problems = problems.filter(rating=rating_filter)

    if tag_filter:
        problems = problems.filter(tags__id__in=tag_filter).distinct()

    if solve_status:
        if solve_status == "solved":
            problems = problems.filter(is_solved=True)
        elif solve_status == "unsolved":
            problems = problems.filter(is_solved=False)

    # Sort problems
    sort_map = {
        "title": "title",
        "rating": "rating",
        "tags": "tags__name",
    }
    problems = problems.order_by(sort_map.get(sort_by, "title"))

    # Get distinct ratings and tags for filters
    distinct_ratings = problems.values_list("rating", flat=True).distinct()
    distinct_tags = Tag.objects.all()

    return render(
        request,
        "problems/problem_list.html",
        {
            "problems": problems,
            "distinct_ratings": distinct_ratings,
            "distinct_tags": distinct_tags,
        },
    )




@login_required(login_url='login')
def create_testcase(request):
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TestCaseForm()
    return render(request, 'problems/create_testcase.html', {'form': form})

@login_required(login_url='login')
def problem_details(request, pk):
    problem = Problem.objects.get(pk=pk)
    example_testcases = TestCase.objects.filter(problem=problem, isExample=True)
    example = {}
    for testcase in example_testcases:
        example[testcase.input_data] = testcase.expected_output
    solved_before = Solved.objects.filter(problem=problem, user=request.user, is_solved = True).exists()
    # Judge0 API configuration
    JUDGE0_API_URL = "https://judge0-ce.p.rapidapi.com/submissions"
    JUDGE0_API_KEY = "c87eb9a9f4msh71ea163f5781cacp191b75jsnad2e6c7d60d5"
    if request.method == "POST":
        # Retrieve the submitted solution and language
        solution = request.POST.get("solution")
        language = request.POST.get("language")

        # Map frontend language selections to Judge0 language IDs
        language_map = {
            "python": 71,
            "c": 50,
            "cpp": 54,
            "java": 62,
        }

        language_id = language_map.get(language)
        if not language_id:
            return JsonResponse({"error": "Invalid language selected."}, status=400)

        # Retrieve test cases for the problem
        test_cases = TestCase.objects.filter(problem=problem)
        all_solved = True
        test_case_results = []

        # Iterate over each test case and send it to Judge0
        for testcase in test_cases:
            input_data = testcase.input_data
            expected_output = testcase.expected_output

            # Prepare payload for Judge0
            payload = {
                "source_code": solution,
                "language_id": language_id,
                "stdin": input_data,
            }
            headers = {
                "Content-Type": "application/json",
                "X-RapidAPI-Key": JUDGE0_API_KEY,
            }

            try:
                # Submit code to Judge0
                submission_response = requests.post(JUDGE0_API_URL, json=payload, headers=headers)
                submission_response.raise_for_status()
                token = submission_response.json().get("token")

                # Poll Judge0 for the result
                result = None
                while True:
                    result_response = requests.get(f"{JUDGE0_API_URL}/{token}", headers=headers)
                    result_response.raise_for_status()
                    result = result_response.json()
                    if result["status"]["id"] == 3:  # Status 3 means "Accepted"
                        break

                # Extract the output and check against expected output
                actual_output = result.get("stdout", "").strip()
                success = actual_output == expected_output.strip()

                if not success:
                    all_solved = False

                test_case_results.append({
                    "input": input_data,
                    "expected": expected_output,
                    "actual": actual_output,
                    "success": success,
                })

            except requests.RequestException as e:
                all_solved = False
                test_case_results.append({
                    "input": input_data,
                    "expected": expected_output,
                    "actual": str(e),
                    "success": False,
                })

        # Update the Solved model
        solved_entry, created = Solved.objects.get_or_create(problem=problem, user=request.user)
        solved_entry.is_solved = all_solved
        solved_entry.save()

        return JsonResponse({"is_solved": all_solved, "solved_before": solved_before})

    
    
    return render(request, "problems/problem_detail.html", {"problem":problem, "test_cases": example, "solved_before": solved_before})