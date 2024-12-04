from django.db import models
from users.models import CustomUser

class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chats")
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Default ordering by creation date
        indexes = [
            models.Index(fields=['user', 'created_at']),  # Index for query optimization
        ]

    def __str__(self):
        return f"{self.user.username} - {self.question[:30]}..." if len(self.question) > 30 else f"{self.user.username} - {self.question}"
    