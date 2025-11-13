from rest_framework import serializers
from .models import Announcement
from users.serializers import UserSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ('id', 'posted_by', 'created_at', 'updated_at')

class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('title', 'body', 'pinned', 'visible_until')