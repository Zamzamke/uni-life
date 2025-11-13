import uuid
from django.db import models
from django.conf import settings

class Opportunity(models.Model):
    CATEGORY_CHOICES = (
        ('internship', 'Internship'),
        ('job', 'Job'),
        ('scholarship', 'Scholarship'),
        ('volunteer', 'Volunteer Work'),
        ('competition', 'Competition'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    deadline = models.DateField()
    requirements = models.JSONField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='opportunities')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['deadline']
        indexes = [
            models.Index(fields=['deadline']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title