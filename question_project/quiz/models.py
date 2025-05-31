from django.db import models
from django.utils.timezone import now

class Question(models.Model):
    text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.text

class QuestionHistory(models.Model):
    ACTION_CHOICES = [
        ('ADD', 'Added'),
        ('EDIT', 'Edited'),
        ('DELETE', 'Deleted'),
    ]
    question_text = models.TextField()
    action = models.CharField(max_length=6, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=now)
    details = models.TextField(blank=True)

    def _str_(self):
        return f"{self.get_action_display()} at {self.timestamp}"