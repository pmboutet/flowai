from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Sponsor, Session
from ..serializers import SponsorSerializer, SessionSerializer

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client']
    search_fields = ['name', 'job_title', 'objectives']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client', None)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        sponsors = []
        errors = []

        for index, item in enumerate(serializer.validated_data):
            try:
                # Vérifie que le client existe
                client_id = item.get('client').id if item.get('client') else None
                if not client_id:
                    raise ValueError('Client est requis pour créer un sponsor')

                sponsor = Sponsor.objects.create(**item)
                sponsors.append(sponsor)
            except Exception as e:
                errors.append({
                    "index": index,
                    "error": str(e)
                })

        response_data = {
            "success": self.get_serializer(sponsors, many=True).data
        }
        if errors:
            response_data["errors"] = errors
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)

        return Response(response_data, status=status.HTTP_201_CREATED)

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client', 'programme']
    search_fields = ['title', 'context', 'objectives']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client', None)
        programme_id = self.request.query_params.get('programme', None)

        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if programme_id:
            queryset = queryset.filter(programme_id=programme_id)

        return queryset

    @action(detail=True, methods=['post'])
    def add_sponsor(self, request, pk=None):
        session = self.get_object()
        sponsor_id = request.data.get('sponsor_id')

        if not sponsor_id:
            return Response(
                {'error': 'sponsor_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sponsor = Sponsor.objects.get(id=sponsor_id)
            # Vérifie que le sponsor appartient au même client que la session
            if sponsor.client_id != session.client_id:
                return Response(
                    {'error': 'Le sponsor doit appartenir au même client que la session'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            session.sponsors.add(sponsor)
            return Response(self.get_serializer(session).data)

        except Sponsor.DoesNotExist:
            return Response(
                {'error': 'Sponsor non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_sponsor(self, request, pk=None):
        session = self.get_object()
        sponsor_id = request.data.get('sponsor_id')

        if not sponsor_id:
            return Response(
                {'error': 'sponsor_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sponsor = Sponsor.objects.get(id=sponsor_id)
            session.sponsors.remove(sponsor)
            return Response(self.get_serializer(session).data)

        except Sponsor.DoesNotExist:
            return Response(
                {'error': 'Sponsor non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def export_summary(self, request, pk=None):
        """Exporte un résumé de la session avec ses séquences"""
        session = self.get_object()
        summary = {
            'title': session.title,
            'context': session.context,
            'objectives': session.objectives,
            'participants': session.participants,
            'design_principles': session.design_principles,
            'sequences': [
                {
                    'title': seq.title,
                    'objective': seq.objective,
                    'order': seq.order,
                    'breakouts': [
                        {
                            'title': bo.title,
                            'objective': bo.objective
                        } for bo in seq.breakouts.all()
                    ]
                } for seq in session.sequences.all().order_by('order')
            ]
        }
        return Response(summary)