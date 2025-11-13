from django.urls import path
from . import views

urlpatterns = [
    path('', views.OpportunityListCreateView.as_view(), name='opportunity-list'),
    path('<uuid:pk>/', views.OpportunityDetailView.as_view(), name='opportunity-detail'),
]