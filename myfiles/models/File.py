from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class File(models.Model):
    FOLDER_CHOICES = [
        ('image', 'Image'), 
        ('video', 'Video')
    ]

    name = models.CharField(
        max_length=255
    )

    file = models.FileField(
        upload_to='uploads/',
        null=True,
        blank=True
    )

    file_type = models.CharField(
        max_length=10, 
        choices=FOLDER_CHOICES
    )

    folder = models.ForeignKey(
        "Folder", 
        on_delete=models.CASCADE, 
        related_name='files', 
        null=True,
        blank=True
    )

    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    size = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
            
            file_extension = self.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                self.file_type = 'image'
            elif file_extension in ['mp4', 'mov', 'avi']:
                self.file_type = 'video'
            else:
                raise ValidationError("Only image and video files are allowed.")

            max_size_mb = 10 if self.file_type == 'image' else 50
            if self.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Maximum file size for {self.file_type}s is {max_size_mb}MB.")
        
        super().save(*args, **kwargs)

    def clean(self):
        pass
