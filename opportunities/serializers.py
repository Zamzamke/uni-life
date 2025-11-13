from rest_framework import serializers
from .models import Opportunity
from users.serializers import UserSerializer

class OpportunitySerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Opportunity
        fields = '__all__'
        read_only_fields = ('id', 'posted_by', 'created_at', 'updated_at')

class OpportunityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ('title', 'description', 'category', 'location', 'deadline', 'requirements')