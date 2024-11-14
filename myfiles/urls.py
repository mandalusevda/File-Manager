from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myfiles/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.HomeView, name='home'),
    path('upload/', views.FileUploadView, name='upload_root'),
    path('upload/<int:folder_id>/', views.FileUploadView, name='upload'), 
    path('view_folder/', views.view_folder, name='view_folder_root'),
    path('view_folder/<int:folder_id>/', views.view_folder, name='view_folder'),
    path('create_folder/', views.create_folder, name='create_folder_root'),
    path('create_folder/<int:folder_id>/', views.create_folder, name='create_folder'),
    path('file/details/<int:file_id>/', views.file_details, name='file_details'),
    path('delete/<int:id>', views.delete_folder, name='delete_folder'),
    path('delete/<int:id>', views.delete_file, name='delete_file'),
    path('rename_file/<int:file_id>/', views.rename_file, name='rename_file'),
    path('rename_folder/<int:folder_id>/', views.rename_folder, name='rename_folder'),
    path('library/', views.library_view, name='library_view'), 
]