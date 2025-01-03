import re
import uuid
from django.db.models import Q
from .models import Client, Programme, Session, Sequence, BreakOut

def model_to_markdown(model_instance, level=1):
    """Convert a model instance to markdown format"""
    model_name = model_instance.__class__.__name__
    header = '#' * level
    markdown = f"{header} [@{model_name}::{model_instance.uuid}]\n\n"

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
    
    if model_type.lower() == 'session':
        markdown = model_to_markdown(instance.client, 1)
        if instance.programme:
            markdown += model_to_markdown(instance.programme, 2)
        markdown += model_to_markdown(instance, 3)
        for sequence in instance.sequences.filter(status='normal').order_by('order'):
            markdown += model_to_markdown(sequence, 4)
            for breakout in sequence.breakouts.filter(status='normal'):
                markdown += model_to_markdown(breakout, 5)
    elif model_type.lower() == 'client':
        markdown = model_to_markdown(instance)
        for programme in instance.programmes.filter(status='normal'):
            markdown += model_to_markdown(programme, 2)
            for session in programme.sessions.filter(status='normal'):
                markdown += model_to_markdown(session, 3)
    elif model_type.lower() == 'programme':
        markdown = model_to_markdown(instance)
        for session in instance.sessions.filter(status='normal'):
            markdown += model_to_markdown(session, 2)
    elif model_type.lower() == 'sequence':
        markdown = model_to_markdown(instance)
        for breakout in instance.breakouts.filter(status='normal'):
            markdown += model_to_markdown(breakout, 2)
    else:
        markdown = model_to_markdown(instance)

    return markdown

def parse_markdown_section(text):
    """Parse a markdown section to extract model type, uuid and fields"""
    header_match = re.search(r'[@(\w+)::(\w+-\w+-\w+-\w+-\w+)]', text)
    if not header_match:
        return None

    model_type, uuid_str = header_match.groups()
    
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

    sections = re.split(r'(?=^#+ \[@)', markdown_text, flags=re.MULTILINE)
    
    processed_uuids = {
        'client': set(),
        'programme': set(),
        'session': set(),
        'sequence': set(),
        'breakout': set()
    }

    created_objects = []
    for section in sections:
        if not section.strip():
            continue
            
        parsed = parse_markdown_section(section)
        if not parsed or parsed['model_type'] not in models:
            continue

        model_class = models[parsed['model_type']]
        
        if parsed['uuid']:
            uuid_obj = uuid.UUID(parsed['uuid'])
            obj, created = model_class.objects.update_or_create(
                uuid=uuid_obj,
                defaults={
                    **parsed['fields'],
                    'status': 'normal'
                }
            )
            processed_uuids[parsed['model_type']].add(uuid_obj)
        else:
            obj = model_class.objects.create(
                **parsed['fields'],
                uuid=uuid.uuid4(),
                status='normal'
            )
            processed_uuids[parsed['model_type']].add(obj.uuid)

        created_objects.append(obj)

    for model_type, uuids in processed_uuids.items():
        models[model_type].objects.filter(
            ~Q(uuid__in=uuids),
            status='normal'
        ).update(status='deleted')

    return created_objects