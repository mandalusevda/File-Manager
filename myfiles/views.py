import json
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404
)

from .models.Folder import Folder
from .models.File import File

from .forms import (
    FileForm, 
    FolderForm,
    RegisterForm
)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'myfiles/register.html', {'form': form})

from django.core.cache import cache
@login_required
def HomeView(request):
    cache_key = f'root_folders_{request.user.id}'
    root_folders = cache.get(cache_key)

    if not root_folders:
        root_folders = Folder.objects.filter(owner=request.user, parent=None).select_related('parent')
        cache.set(cache_key, root_folders, 60 * 15)
    
    return render(request, 'myfiles/home.html', {'folders': root_folders})

@login_required
def FileUploadView(request, folder_id=None):
    folder = get_object_or_404(Folder, id=folder_id) if folder_id else None
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return HttpResponseForbidden("No file was uploaded.")
        if uploaded_file.content_type not in ['image/jpeg', 'image/png', 'video/mp4']:
            return HttpResponseForbidden("Only image and video files are allowed.")
        if uploaded_file.size > 50 * 1024 * 1024:
            return HttpResponseForbidden("File size exceeds the allowed limit.")

        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.folder = folder
            file.size = file.file.size
            file.save()
            return redirect('home')
    else:
        form = FileForm()
    return render(request, 'myfiles/upload.html', {'form': form, 'folder': folder})

def file_details(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return render(request, 'myfiles/file_details.html', {'file': file})


@login_required
def view_folder(request, folder_id=None):
    if folder_id is None:
        folder = None
        subfolders = Folder.objects.filter(parent=None, owner=request.user).select_related('parent')
        files = File.objects.filter(folder=None, owner=request.user).select_related('folder', 'owner')
    else:
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        subfolders = Folder.objects.filter(parent=folder)
        files = File.objects.filter(folder=folder)

    query = request.GET.get('query')
    if query:
        files = files.filter(name__icontains=query)

    # Generate breadcrumbs for navigation
    breadcrumbs = []
    current_folder = folder
    while current_folder:
        breadcrumbs.insert(0, current_folder)
        current_folder = current_folder.parent

    return render(request, 
        'myfiles/folder_view.html', {
        'folder': folder,
        'subfolders': subfolders,
        'files': files,
        'breadcrumbs': breadcrumbs,
    })

@login_required
def create_folder(request, folder_id=None):
    # Get the parent folder if folder_id is provided
    parent_folder = get_object_or_404(Folder, id=folder_id, owner=request.user) if folder_id else None

    if request.method == 'POST':
        form = FolderForm(request.POST)
        
        if form.is_valid():
            # Extract folder name from the form
            folder_name = form.cleaned_data.get('name')

            # Default to "New Folder" if the name is empty
            if not folder_name:
                folder_name = "New Folder"

            # Ensure the folder name is unique within the user's folders, including parent folder context
            original_name = folder_name
            counter = 1
            while Folder.objects.filter(name=folder_name, owner=request.user, parent=parent_folder).exists():
                folder_name = f"{original_name} ({counter})"
                counter += 1
            
            # Create the new folder and associate it with the current user and the parent folder (if any)
            new_folder = form.save(commit=False)
            new_folder.owner = request.user
            new_folder.parent = parent_folder
            new_folder.name = folder_name  # Set the final folder name after ensuring uniqueness
            new_folder.save()

            # Redirect to the folder view page
            if parent_folder:
                return redirect('view_folder', folder_id=parent_folder.id)
            else:
                return redirect('view_folder_root')
    
    else:
        form = FolderForm()

    # Render the form and pass the parent folder (if any)
    return render(request, 'myfiles/create_folder.html', {
        'form': form,
        'parent_folder': parent_folder,
    })


def delete_folder(request, id):
    Folder.objects.filter(id=id, owner=request.user).delete()
    messages.success(request, "Folder deleted successfully.")
    return redirect("home")


def delete_file(request, id):
    File.objects.filter(id=id, owner=request.user).delete()
    messages.success(request, "File deleted successfully.")
    return redirect("home")

@login_required
@require_POST
def rename_file(request, file_id):
    try:
        file = File.objects.get(id=file_id, owner=request.user)
        data = json.loads(request.body)
        new_name = data.get('new_name')

        if not new_name:
            return JsonResponse({"success": False, "error": "File name cannot be empty."})

        file.name = new_name
        file.save()
        return JsonResponse({"success": True})
    except File.DoesNotExist:
        return JsonResponse({"success": False, "error": "File not found."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@login_required
@require_POST
def rename_folder(request, folder_id):
    try:
        folder = Folder.objects.get(id=folder_id, owner=request.user)
        data = json.loads(request.body)
        new_name = data.get('new_name')

        if not new_name:
            return JsonResponse({"success": False, "error": "Folder name cannot be empty."})

        folder.name = new_name
        folder.save()
        return JsonResponse({"success": True})
    except Folder.DoesNotExist:
        return JsonResponse({"success": False, "error": "Folder not found."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
@login_required
def library_view(request):
    # view for searching items
    query = request.GET.get('query', '')
    folders = Folder.objects.filter(owner=request.user)
    if query:
        files = File.objects.filter(
            Q(name__icontains=query),
            owner=request.user
        )
    else:
        files = File.objects.filter(owner=request.user)

    context = {
        'folders': folders,
        'files': files,
        'query': query,
    }
    return render(request, 'myfiles/home.html', context)