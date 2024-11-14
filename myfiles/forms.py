from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models.Folder import Folder
from .models.File import File

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = [
            "username", 
            "email", 
            "password1", 
            "password2"
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'name', 
            'file',
        ]
        
    def clean_file(self):
        file = self.cleaned_data['file']
        if not file:
            raise forms.ValidationError("No file uploaded.")
        
        # Use file extension as a workaround to check type
        valid_image_extensions = ['jpg', 'jpeg', 'png']
        valid_video_extensions = ['mp4']
        file_extension = file.name.split('.')[-1].lower()

        if file_extension in valid_image_extensions and file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Image file size cannot exceed 10MB.")
        elif file_extension in valid_video_extensions and file.size > 50 * 1024 * 1024:
            raise forms.ValidationError("Video file size cannot exceed 50MB.")
        elif file_extension not in valid_image_extensions + valid_video_extensions:
            raise forms.ValidationError("Only JPEG, PNG images, and MP4 videos are allowed.")
        
        return file


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Folder Name'}),
        }
        labels = {
            'name': 'Folder Name',
        }