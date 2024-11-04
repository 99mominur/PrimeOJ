# contests/models.py
from django.db import models
from users.models import CustomUser
from problems.models import Problem
class Contest(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    CONTEST_TYPES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type = models.CharField(max_length=10, choices=CONTEST_TYPES, default=PUBLIC)
    key = models.CharField(max_length=100, blank=True, null=True)  # for private contests

    invited_users = models.ManyToManyField(CustomUser, blank=True, related_name='invitations')
    problems = models.ManyToManyField(Problem, blank=False, null=False)
    
    def __str__(self):
        return self.name
