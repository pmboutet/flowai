from rest_framework import serializers
from .models import (Conversation, Client, Programme, Sponsor, 
                    Session, Sequence, BreakOut)

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'created_at', 'updated_at', 'provider', 
                 'user_input', 'ai_response', 'prompt_tokens', 
                 'completion_tokens', 'total_tokens']
        read_only_fields = ['created_at', 'updated_at', 'ai_response', 
                          'prompt_tokens', 'completion_tokens', 'total_tokens']

class BreakOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakOut
        fields = ['id', 'title', 'sequence', 'description', 'objective', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SequenceSerializer(serializers.ModelSerializer):
    breakouts = BreakOutSerializer(many=True, read_only=True)

    class Meta:
        model = Sequence
        fields = ['id', 'title', 'session', 'objective', 'input_drive_url', 
                 'input_text', 'output_drive_url', 'output_text', 'order', 
                 'breakouts', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
