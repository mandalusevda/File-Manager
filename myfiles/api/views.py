
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema_view, 
    extend_schema
)
from rest_framework import (
    viewsets, 
    status,
    serializers
)
from rest_framework.filters import (
    SearchFilter, 
    OrderingFilter
)
from rest_framework.permissions import (
    AllowAny, 
    IsAdminUser, 
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import (
    MultiPartParser, 
    FormParser
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from .paginations import DefaultPagination

from myfiles.models.Folder import Folder
from myfiles.models.File import File

from .seriailizers import (
    FolderSerializer,
    FileSerializer
)


@extend_schema_view(
    create=extend_schema(tags=["Folder"], summary="Create a new Folder"),
    retrieve=extend_schema(tags=["Folder"], summary="Retrieve a single Folder."),
    list=extend_schema(tags=["Folder"], summary="Retrieve a list of Folders"),
    update=extend_schema(tags=["Folder"], summary="Update a Folder"),
    partial_update=extend_schema(tags=["Folder"], summary="Partial update a Folder"),
    destroy=extend_schema(tags=["Folder"], summary="Deletes a Folder"),
)

class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    lookup_field='id'
    lookup_url_kwarg = 'id'

    # Filter options
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = [
        'parent', 
        'created_at'
    ]
    search_fields = [
        'name'
    ]
    ordering_fields = [
        'name',
        'created_at'
    ]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    ACTION_PERMISSIONS = {
        "list": [AllowAny()],
        "retrieve": [AllowAny()],
        "list_variants": [AllowAny()],
    }

    def get_permissions(self):
        return self.ACTION_PERMISSIONS.get(self.action, super().get_permissions())

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        parent_id = self.request.query_params.get('parent', None)
        if parent_id:
            return Folder.objects.filter(parent_id=parent_id)
        return Folder.objects.all()
    

@extend_schema_view(
    create=extend_schema(tags=["File"], summary="Create a new File"),
    retrieve=extend_schema(tags=["File"], summary="Retrieve a single File"),
    list=extend_schema(tags=["File"], summary="Retrieve a list of Files"),
    update=extend_schema(tags=["File"], summary="Update an File"),
    destroy=extend_schema(tags=["File"], summary="Deletes an File"),
)
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    lookup_field='id'
    lookup_url_kwarg = 'id'

    # Filter options
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = [
        'folder', 
        'file_type', 
        'created_at'
    ]
    search_fields = [
        'name'
    ]
    ordering_fields = [
        "size",
        "name", 
        'created_at'
    ]
    pagination_class = DefaultPagination

    ACTION_PERMISSIONS = {
        "list": [AllowAny()],
        "retrieve": [AllowAny()],
    }

    def get_permissions(self):
        return self.ACTION_PERMISSIONS.get(self.action, super().get_permissions())

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        folder_id = self.request.query_params.get('folder', None)
        if folder_id:
            return File.objects.filter(folder_id=folder_id)
        return File.objects.all()