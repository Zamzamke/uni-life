from django.shortcuts import render
from rest_framework import generics, permissions
from django.utils import timezone
from django.db.models import Q
from .models import Opportunity
from .serializers import OpportunitySerializer, OpportunityCreateSerializer
from announcements.views import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class OpportunityListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Opportunity.objects.filter(verified=True)
        
        # Filter out expired opportunities
        queryset = queryset.filter(deadline__gte=timezone.now().date())
        
        # Apply filters from query parameters
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        deadline_before = self.request.query_params.get('deadline_before')
        if deadline_before:
            queryset = queryset.filter(deadline__lte=deadline_before)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OpportunityCreateSerializer
        return OpportunitySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @swagger_auto_schema(
        operation_description="Get all verified and active opportunities",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description='Filter by category (internship, job, scholarship, volunteer, competition)',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'deadline_before',
                openapi.IN_QUERY,
                description='Filter by deadline before date (YYYY-MM-DD)',
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={200: OpportunitySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new opportunity (Admin only)",
        request_body=OpportunitySerializer,
        responses={
            201: OpportunitySerializer,
            403: 'Permission denied - Admin access required'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class OpportunityDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

    @swagger_auto_schema(
        operation_description="Get a specific opportunity by ID",
        responses={200: OpportunitySerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)