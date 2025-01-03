import re
import uuid
from django.db.models import Q
from ..models import Client, Programme, Session, Sequence, BreakOut

def parse_markdown_section(text):
    # Amélioration du regex pour la détection des sections
    header_match = re.search(r'\[@(\w+)::([\w-]+)\]', text)
    if not header_match:
        return None

    model_type, uuid_str = header_match.groups()
    
    # Amélioration du regex pour l'extraction des champs
    fields = {}
    for line in text.split('\n'):
        field_match = re.match(r'\*\*(\w+)\*\*:\s*([^\n]+)', line)
        if field_match:
            field_name, value = field_match.groups()
            fields[field_name] = value.strip()
            
    return {
        'model_type': model_type.lower(),
        'uuid': uuid_str,
        'fields': fields
    }