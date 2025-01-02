import os
from abc import ABC, abstractmethod
from openai import OpenAI
import requests
from django.conf import settings

class AIProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt):
        pass

class OpenAIProvider(AIProvider):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def generate_response(self, prompt):
        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant IA utile et professionnel."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            'response': completion.choices[0].message.content,
            'prompt_tokens': completion.usage.prompt_tokens,
            'completion_tokens': completion.usage.completion_tokens,
            'total_tokens': completion.usage.total_tokens
        }

class GrokProvider(AIProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = settings.GROK_API_URL
    
    def generate_response(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messages': [
                {"role": "system", "content": "Vous êtes un assistant IA utile et professionnel."},
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        response.raise_for_status()
        result = response.json()
        
        return {
            'response': result['choices'][0]['message']['content'],
            'prompt_tokens': result['usage']['prompt_tokens'],
            'completion_tokens': result['usage']['completion_tokens'],
            'total_tokens': result['usage']['total_tokens']
        }

class AIService:
    providers = {
        'openai': OpenAIProvider,
        'grok': GrokProvider
    }
    
    @classmethod
    def get_provider(cls, provider_name):
        if provider_name not in cls.providers:
            raise ValueError(f"Provider {provider_name} not supported")
            
        if provider_name == 'openai':
            api_key = settings.OPENAI_API_KEY
        else:  # grok
            api_key = settings.GROK_API_KEY
            
        return cls.providers[provider_name](api_key)