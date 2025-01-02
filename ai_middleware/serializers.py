from rest_framework import serializers
from .models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'created_at', 'updated_at', 'provider', 
                 'user_input', 'ai_response', 'prompt_tokens', 
                 'completion_tokens', 'total_tokens']
        read_only_fields = ['created_at', 'updated_at', 'ai_response', 
                          'prompt_tokens', 'completion_tokens', 'total_tokens']