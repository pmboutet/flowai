from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..services.markdown_service import to_markdown, from_markdown
from ..models import Client, Programme, Session, Sequence, BreakOut

class MarkdownExportView(views.APIView):
    def get(self, request, uuid=None, model_type=None, pk=None):
        try:
            if uuid:
                # Recherche par UUID
                for model in [Client, Programme, Session, Sequence, BreakOut]:
                    try:
                        obj = get_object_or_404(model, uuid=uuid)
                        markdown = to_markdown(obj)
                        return Response({'markdown': markdown})
                    except model.DoesNotExist:
                        continue
                return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
                
            elif model_type and pk:
                # Recherche par type de modèle et ID
                models = {
                    'client': Client,
                    'programme': Programme,
                    'session': Session,
                    'sequence': Sequence,
                    'breakout': BreakOut
                }
                model = models.get(model_type.lower())
                if not model:
                    return Response({'error': 'Invalid model type'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Essayer de trouver l'objet par ID ou UUID
                obj = get_object_or_404(model, pk=pk)
                markdown = to_markdown(obj)
                return Response({'markdown': markdown})
            
            return Response({'error': 'UUID or model_type and pk are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MarkdownImportView(views.APIView):
    def post(self, request):
        try:
            markdown = request.data.get('markdown')
            if not markdown:
                return Response({'error': 'Markdown content is required'}, 
                               status=status.HTTP_400_BAD_REQUEST)
            
            objects = from_markdown(markdown)
            return Response({'message': f'{len(objects)} objects processed'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)