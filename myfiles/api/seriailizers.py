from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField
)
from myfiles.models.Folder import Folder
from myfiles.models.File import File

class FolderSerializer(ModelSerializer):
    parent = PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Folder
        fields = [
            'id',
            'name',
            'owner',
            'parent',
            'created_at',
            'updated_at'
        ]

class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id", 
            "name", 
            "file", 
            "file_type", 
            "folder", 
            "owner", 
            "updated_at",
            "created_at",
            "size"
        ]
