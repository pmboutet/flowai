from django.apps import AppConfig

class FlowAIConfig(AppConfig):
    name = 'flowai'
    verbose_name = 'FlowAI'
    
    def ready(self):
        # Import the patching function and apply the patch
        from .patches import apply_patches
        apply_patches()