from django import forms
from .models import Problem, TestCase

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = "__all__"

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = "__all__"