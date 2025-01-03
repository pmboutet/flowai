import re
import uuid
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
    markdown = model_to_markdown(instance)

    # Add related objects based on model type
    if model_type.lower() == 'client':
        for programme in instance.programmes.filter(status='normal'):
            markdown += model_to_markdown(programme, 2)
            for session in programme.sessions.filter(status='normal'):
                markdown += model_to_markdown(session, 3)

    elif model_type.lower() == 'programme':
        for session in instance.sessions.filter(status='normal'):
            markdown += model_to_markdown(session, 2)

    elif model_type.lower() == 'session':
        for sequence in instance.sequences.filter(status='normal').order_by('order'):
            markdown += model_to_markdown(sequence, 2)
            for breakout in sequence.breakouts.filter(status='normal'):
                markdown += model_to_markdown(breakout, 3)

    elif model_type.lower() == 'sequence':
        for breakout in instance.breakouts.filter(status='normal'):
            markdown += model_to_markdown(breakout, 2)

    return markdown

def parse_markdown_section(text):
    """Parse a markdown section to extract model type, uuid and fields"""
    # Extract model type and uuid from header
    header_match = re.search(r'[@(\w+)::(\w+-\w+-\w+-\w+-\w+)]', text)
    if not header_match:
        return None

    model_type, uuid_str = header_match.groups()
    
    # Extract fields
    fields = {}
    for line in text.split('\n'):
        field_match = re.match(r'\*\*(\w+)\*\*:\s*(.+)', line)
        if field_match:
            field_name, value = field_match.groups()
            fields[field_name] = value.strip()
            
    return {
        'model_type': model_type.lower(),
        'uuid': uuid_str,
        'fields': fields
    }

def from_markdown(markdown_text):
    """Create or update objects from markdown text"""
    models = {
        'client': Client,
        'programme': Programme,
        'session': Session,
        'sequence': Sequence,
        'breakout': BreakOut
    }

    # Split markdown into sections based on headers
    sections = re.split(r'(?=^#+ \[@)', markdown_text, flags=re.MULTILINE)
    
    # Process each section
    created_objects = []
    for section in sections:
        if not section.strip():
            continue
            
        parsed = parse_markdown_section(section)
        if not parsed:
            continue

        model_class = models.get(parsed['model_type'])
        if not model_class:
            continue

        # Create or update object
        if parsed['uuid']:
            obj, created = model_class.objects.update_or_create(
                uuid=uuid.UUID(parsed['uuid']),
                defaults={
                    **parsed['fields'],
                    'status': 'normal'
                }
            )
        else:
            obj = model_class.objects.create(
                **parsed['fields'],
                uuid=uuid.uuid4(),
                status='normal'
            )

        created_objects.append(obj)

    # Mark objects as deleted if they're not in the markdown
    # This depends on the hierarchy of objects and should be implemented based on requirements

    return created_objects