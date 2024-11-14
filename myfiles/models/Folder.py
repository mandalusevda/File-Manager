from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )

    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subfolders'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
