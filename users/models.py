# models.py
from django.db import models
from django.contrib.auth.models import User

class UserInputOutput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    input_question = models.TextField()
    output_recommendations = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Input from {self.user} on {self.timestamp}"
