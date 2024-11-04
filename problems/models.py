from django.db import models
from users.models import CustomUser

class Problem(models.Model):
    seter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    example = models.TextField()
    rating = models.IntegerField()
    tags = models.CharField(max_length=255)
    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases', null=False, blank=False)
    input_data = models.TextField(null=False, blank=False)
    expected_output = models.TextField(null=False, blank=False)
