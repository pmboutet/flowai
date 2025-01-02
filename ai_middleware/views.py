import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation
from .serializers import ConversationSerializer
from openai import OpenAI
from django.conf import settings

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant IA utile et professionnel."},
                    {"role": "user", "content": serializer.validated_data['user_input']}
                ]
            )

            conversation = Conversation.objects.create(
                user_input=serializer.validated_data['user_input'],
                ai_response=completion.choices[0].message.content,
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )

            serializer = self.get_serializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )