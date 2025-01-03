from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Conversation
from ..serializers import ConversationSerializer
from ..services import AIService

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            provider = serializer.validated_data.get('provider', 'grok')
            ai_service = AIService.get_provider(provider)
            
            result = ai_service.generate_response(
                serializer.validated_data['user_input']
            )
            
            conversation = Conversation.objects.create(
                provider=provider,
                user_input=serializer.validated_data['user_input'],
                ai_response=result['response'],
                prompt_tokens=result['prompt_tokens'],
                completion_tokens=result['completion_tokens'],
                total_tokens=result['total_tokens']
            )

            serializer = self.get_serializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        
        conversations = []
        errors = []
        for index, item in enumerate(serializer.validated_data):
            try:
                provider = item.get('provider', 'grok')
                ai_service = AIService.get_provider(provider)
                
                result = ai_service.generate_response(item['user_input'])
                
                conversation = Conversation.objects.create(
                    provider=provider,
                    user_input=item['user_input'],
                    ai_response=result['response'],
                    prompt_tokens=result['prompt_tokens'],
                    completion_tokens=result['completion_tokens'],
                    total_tokens=result['total_tokens']
                )
                conversations.append(conversation)
                
            except Exception as e:
                errors.append({
                    "index": index,
                    "error": str(e)
                })
        
        response_data = {
            "success": self.get_serializer(conversations, many=True).data
        }
        if errors:
            response_data["errors"] = errors
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
            
        return Response(response_data, status=status.HTTP_201_CREATED)