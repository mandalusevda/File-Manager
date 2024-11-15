import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from myfiles.models.Folder import Folder
from myfiles.models.File import File

class LibraryTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create a test folder
        self.folder = Folder.objects.create(name="Test Folder", owner=self.user)
        
        # Create a test file
        self.file = File.objects.create(
            name="Test File",
            folder=self.folder,
            owner=self.user,
            file=SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpeg"),
            file_type="image",
            size=1024
        )

    def test_create_folder(self):
        response = self.client.post(reverse('create_folder', args=[self.folder.id]), {'name': 'New Folder'})
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Folder.objects.filter(name="New Folder").exists())

    def test_rename_folder_success(self):
        response = self.client.post(
            reverse('rename_folder', args=[self.folder.id]),
            json.dumps({'new_name': 'Renamed Folder'}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})

        self.folder.refresh_from_db()
        self.assertEqual(self.folder.name, 'Renamed Folder')

    def test_search_files_and_folders(self):
        # Test search for folder
        response = self.client.get(reverse('library_view'), {'query': 'Test Folder'})
        self.assertContains(response, 'Test Folder')