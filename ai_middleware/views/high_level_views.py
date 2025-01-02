from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from ..models import Programme, Client
from ..serializers import (ProgrammeSerializer, ClientSerializer,
                         ClientLightSerializer, SessionSerializer)

class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client', None)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Retourne des statistiques sur le programme"""
        programme = self.get_object()
        stats = {
            'total_sessions': programme.sessions.count(),
            'total_sequences': sum(session.sequences.count() 
                                 for session in programme.sessions.all()),
            'sessions_by_status': programme.sessions.values('status')
                .annotate(count=Count('id')),
            'participants_count': sum(len(session.participants.split(',')) 
                                   for session in programme.sessions.all() 
                                   if session.participants)
        }
        return Response(stats)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'context', 'objectives']
    ordering_fields = ['name', 'created_at']

    def get_serializer_class(self):
        # Utilise le sérialiseur allégé pour les listes
        if self.action == 'list':
            return ClientLightSerializer
        return ClientSerializer

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Retourne un tableau de bord pour le client"""
        client = self.get_object()
        
        # Statistiques générales
        total_sessions = client.sessions.count()
        total_programmes = client.programmes.count()
        total_sponsors = client.sponsors.count()
        
        # Sessions récentes
        recent_sessions = client.sessions.order_by('-created_at')[:5]
        
        # Programmes actifs
        active_programmes = client.programmes.annotate(
            session_count=Count('sessions')
        ).filter(session_count__gt=0)
        
        dashboard_data = {
            'statistics': {
                'total_sessions': total_sessions,
                'total_programmes': total_programmes,
                'total_sponsors': total_sponsors,
            },
            'recent_sessions': SessionSerializer(recent_sessions, many=True).data,
            'active_programmes': ProgrammeSerializer(active_programmes, many=True).data
        }
        
        return Response(dashboard_data)

    @action(detail=True, methods=['post'])
    def analyze_with_ai(self, request, pk=None):
        """Analyse les données du client avec l'IA pour générer des recommandations"""
        client = self.get_object()
        
        # Prépare le contexte pour l'IA
        context = f"""Client: {client.name}
Contexte: {client.context}
Objectifs: {client.objectives}

"""
        
        # Ajoute les informations sur les sessions
        for session in client.sessions.all():
            context += f"""Session: {session.title}
Objectifs: {session.objectives}
Principes de design: {session.design_principles}

"""
        
        # Utilise le service AI pour générer des recommandations
        try:
            from ..services import AIService
            ai_service = AIService.get_provider('grok')
            result = ai_service.generate_response(
                f"En tant qu'expert en design de session collaborative, analyse les "
                f"données suivantes et propose des recommandations pour améliorer "
                f"les futures sessions:\n\n{context}"
            )
            
            return Response({
                'recommendations': result['response'],
                'analysis_details': {
                    'tokens_used': result['total_tokens'],
                    'analyzed_sessions': client.sessions.count()
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de l\'analyse IA: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )