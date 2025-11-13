from django.urls import path
from . import views

urlpatterns = [
    path('', views.AnnouncementListCreateView.as_view(), name='announcement-list'),
    path('<uuid:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
]