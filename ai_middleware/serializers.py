from rest_framework import serializers
from .models import Client, Programme, Session, Sequence, BreakOut

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = '__all__'

class BreakOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakOut
        fields = '__all__'