import re
import uuid
from django.db.models import Q
from .models import Client, Programme, Session, Sequence, BreakOut

def model_to_markdown(model_instance, level=1):
    """Convert a model instance to markdown format"""
    model_name = model_instance.__class__.__name__
    header = '#' * level
    markdown = f"{header} [@{model_name}::{model_instance.uuid}]\n\n"

    # Add all fields
    for field in model_instance._meta.fields:
        if field.name not in ['id', 'uuid', 'created_at', 'updated_at', 'status']:
            value = getattr(model_instance, field.name)
            if value and not field.is_relation:
                markdown += f"**{field.name}**: {value}\n\n"

    return markdown

def to_markdown(uuid_str, model_type):
    """Generate markdown for a model and its relations"""
    models = {
        'client': Client,
        'programme': Programme,
        'session': Session,
        'sequence': Sequence,
        'breakout': BreakOut
    }

    if model_type.lower() not in models:
        raise ValueError(f"Invalid model type: {model_type}")

    model_class = models[model_type.lower()]
    instance = model_class.objects.get(uuid=uuid_str)
    
    # If we're starting from a session, also get client and programme
    if model_type.lower() == 'session':
        markdown = model_to_markdown(instance.client, 1)
        if instance.programme:
            markdown += model_to_markdown(instance.programme, 2)
        markdown += model_to_markdown(instance, 3)
        for sequence in instance.sequences.filter(status='normal').order_by('order'):
            markdown += model_to_markdown(sequence, 4)
            for breakout in sequence.breakouts.filter(status='normal'):
                markdown += model_to_markdown(breakout, 5)
    else:
        markdown = model_to_markdown(instance)
        # [Rest of the code remains the same]

    return markdown

[Rest of the file remains the same]