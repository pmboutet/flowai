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

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'job_title', 'objectives', 'client', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SessionSerializer(serializers.ModelSerializer):
    sequences = SequenceSerializer(many=True, read_only=True)
    sponsors = SponsorSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'title', 'programme', 'client', 'context', 
                 'objectives', 'inputs', 'outputs', 'participants', 
                 'design_principles', 'deliverables', 'sponsors', 
                 'sequences', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProgrammeSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)

    class Meta:
        model = Programme
        fields = ['id', 'name', 'client', 'description', 'sessions', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ClientSerializer(serializers.ModelSerializer):
    programmes = ProgrammeSerializer(many=True, read_only=True)
    sponsors = SponsorSerializer(many=True, read_only=True)
    sessions = SessionSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'context', 'objectives', 'programmes', 
                 'sponsors', 'sessions', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ClientLightSerializer(serializers.ModelSerializer):
    """Version allégée du sérialiseur Client pour les listes et les références"""
    class Meta:
        model = Client
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']