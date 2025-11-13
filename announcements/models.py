import uuid
from django.db import models
from django.conf import settings

class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')
    pinned = models.BooleanField(default=False)
    visible_from = models.DateTimeField(auto_now_add=True)
    visible_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-pinned', '-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['visible_until']),
        ]
    
    def __str__(self):
        return self.title
