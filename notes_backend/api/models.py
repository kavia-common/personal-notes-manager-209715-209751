from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    """Note entity representing a personal note owned by a user."""
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.title} (#{self.pk})"
