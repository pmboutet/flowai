from rest_framework import views, status
from rest_framework.response import Response
from ..services.markdown_service import to_markdown, from_markdown
from ..models import Client, Programme, Session, Sequence, BreakOut

class MarkdownExportView(views.APIView):
    def get(self, request, uuid=None, model_type=None, pk=None):
        try:
            if uuid:
                for model in [Client, Programme, Session, Sequence, BreakOut]:
                    try:
                        obj = model.objects.get(uuid=uuid)
                        markdown = to_markdown(uuid, model.__name__.lower())
                        return Response({'markdown': markdown})
                    except model.DoesNotExist:
                        continue
            elif model_type and pk:
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
                obj = model.objects.get(id=pk)
                markdown = to_markdown(obj.uuid, model_type)
                return Response({'markdown': markdown})
                
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)