from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class AnnouncementListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Announcement.objects.all()
        # Filter active announcements
        now = timezone.now()
        queryset = queryset.filter(visible_from__lte=now)
        queryset = queryset.filter(models.Q(visible_until__isnull=True) | models.Q(visible_until__gte=now))
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnnouncementCreateSerializer
        return AnnouncementSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @swagger_auto_schema(
        operation_description="Get all active announcements",
        responses={200: AnnouncementSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description='JWT Token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new announcement (Admin only)",
        request_body=AnnouncementSerializer,
        responses={
            201: AnnouncementSerializer,
            403: 'Permission denied - Admin access required'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AnnouncementDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    @swagger_auto_schema(
        operation_description="Get a specific announcement by ID",
        responses={200: AnnouncementSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
