from rest_framework import views, status
from rest_framework.response import Response
from .services import to_markdown, from_markdown

class MarkdownExportView(views.APIView):
    def get(self, request, model_type, uuid):
        try:
            markdown = to_markdown(uuid, model_type)
            return Response({'markdown': markdown})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MarkdownImportView(views.APIView):
    def post(self, request):
        try:
            markdown = request.data.get('markdown')
            if not markdown:
                return Response({'error': 'Markdown content is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            objects = from_markdown(markdown)
            return Response({'message': f'{len(objects)} objects processed'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)