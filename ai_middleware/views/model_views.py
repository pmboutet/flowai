from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models import Client, Programme, Session, Sequence, BreakOut
from ..serializers import ClientSerializer, ProgrammeSerializer, SessionSerializer, SequenceSerializer, BreakOutSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.exclude(status='deleted')
    serializer_class = ClientSerializer

class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = Programme.objects.exclude(status='deleted')
    serializer_class = ProgrammeSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.exclude(status='deleted')
    serializer_class = SessionSerializer

class SequenceViewSet(viewsets.ModelViewSet):
    queryset = Sequence.objects.exclude(status='deleted')
    serializer_class = SequenceSerializer

class BreakOutViewSet(viewsets.ModelViewSet):
    queryset = BreakOut.objects.exclude(status='deleted')
    serializer_class = BreakOutSerializer