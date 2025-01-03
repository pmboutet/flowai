import re
import uuid
from django.db.models import Q
from .models import Client, Programme, Session, Sequence, BreakOut

# [Previous code remains the same until from_markdown function]

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
    
    # Keep track of processed UUIDs
    processed_uuids = {
        'client': set(),
        'programme': set(),
        'session': set(),
        'sequence': set(),
        'breakout': set()
    }

    # Process each section
    created_objects = []
    for section in sections:
        if not section.strip():
            continue
            
        parsed = parse_markdown_section(section)
        if not parsed or parsed['model_type'] not in models:
            continue

        model_class = models[parsed['model_type']]
        
        # Create or update object
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

    # Mark unused objects as deleted
    for model_type, uuids in processed_uuids.items():
        models[model_type].objects.filter(
            ~Q(uuid__in=uuids),
            status='normal'
        ).update(status='deleted')

    return created_objects