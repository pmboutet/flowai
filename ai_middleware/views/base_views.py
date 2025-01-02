from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from ..models import BreakOut, Sequence
from ..serializers import BreakOutSerializer, SequenceSerializer

class BreakOutViewSet(viewsets.ModelViewSet):
    queryset = BreakOut.objects.all()
    serializer_class = BreakOutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sequence']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()
        sequence_id = self.request.query_params.get('sequence', None)
        if sequence_id:
            queryset = queryset.filter(sequence_id=sequence_id)
        return queryset

class SequenceViewSet(viewsets.ModelViewSet):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['session']
    search_fields = ['title', 'objective']
    ordering_fields = ['order', 'created_at', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()
        session_id = self.request.query_params.get('session', None)
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        return queryset

    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        sequence = self.get_object()
        new_order = request.data.get('order')
        
        if new_order is None:
            return Response(
                {'error': 'Le paramètre order est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Déplacer les autres séquences si nécessaire
        if new_order > sequence.order:
            Sequence.objects.filter(
                session=sequence.session,
                order__gt=sequence.order,
                order__lte=new_order
            ).update(order=models.F('order') - 1)
        else:
            Sequence.objects.filter(
                session=sequence.session,
                order__gte=new_order,
                order__lt=sequence.order
            ).update(order=models.F('order') + 1)
            
        sequence.order = new_order
        sequence.save()
        
        return Response(self.get_serializer(sequence).data)