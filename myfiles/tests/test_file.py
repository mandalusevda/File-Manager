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

    def test_create_file(self):
        self.user.is_staff = True
        self.user.save()

        # Ensure the file exists for upload
        with open('testfile.jpg', 'wb') as f:
            f.write(b"Test content")  
        
        with open('testfile.jpg', 'rb') as f:
            response = self.client.post(reverse('upload', args=[self.folder.id]), {
                'file': f,
                'name': 'New File',
            })

        self.assertEqual(response.status_code, 302) 
        self.assertTrue(File.objects.filter(name="New File").exists())

    def test_rename_file_success(self):
        new_name = "Renamed File"
        response = self.client.post(
            reverse('rename_file', args=[self.file.id]),
            data=json.dumps({'new_name': new_name}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})

        self.file.refresh_from_db()
        self.assertEqual(self.file.name, new_name)

    def test_search_files_and_folders(self):
        # Test search for file
        response = self.client.get(reverse('library_view'), {'query': 'Test File'})
        self.assertContains(response, 'Test File')