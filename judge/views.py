
# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from problems.models import Problem


# JUDGE0_URL = "https://api.judge0.com/submissions"

# def submit_code(request):
#     if request.method == 'POST':
#         code = request.POST['code']
#         language_id = request.POST['language_id']
#         problem_id = request.POST['problem_id']
#         problem = Problem.objects.get(id=problem_id)

#         results = []
#         for test_case in problem.test_cases.all():
#             data = {
#                 "source_code": code,
#                 "language_id": language_id,
#                 "stdin": test_case.input_data,
#                 "expected_output": test_case.expected_output
#             }
#             response = requests.post(JUDGE0_URL, json=data)
#             results.append(response.json())

#         return JsonResponse({"results": results})
