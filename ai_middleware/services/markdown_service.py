import re
import uuid
from django.db.models import Q
from ..models import Client, Programme, Session, Sequence, BreakOut

def model_to_markdown(model_instance, level=1):
    """
    Convertit une instance de modèle en texte Markdown.
    
    Args:
        model_instance: Instance du modèle Django à convertir
        level: Niveau de titre Markdown (profondeur hiérarchique)
    
    Returns:
        str: Représentation Markdown de l'instance
    """
    model_name = model_instance.__class__.__name__
    header = '#' * level
    markdown = f"{header} [@{model_name}::{model_instance.uuid}]\n\n"

    # Parcourt les champs en ignorant les champs système
    for field in model_instance._meta.fields:
        if field.name not in ['id', 'uuid', 'created_at', 'updated_at', 'status']:
            value = getattr(model_instance, field.name)
            if value and not field.is_relation:
                markdown += f"**{field.name}**: {value}\n\n"

    return markdown

def to_markdown(uuid_str, model_type):
    """
    Convertit un objet en Markdown basé sur son UUID et son type.
    
    Args:
        uuid_str: UUID de l'instance
        model_type: Type de modèle (client, programme, session, etc.)
    
    Returns:
        str: Représentation Markdown de l'objet
    """
    # Dictionnaire de mappage des types de modèles
    models = {
        'client': Client,
        'programme': Programme,
        'session': Session,
        'sequence': Sequence,
        'breakout': BreakOut
    }

    # Validation du type de modèle
    if model_type.lower() not in models:
        raise ValueError(f"Invalid model type: {model_type}")

    model_class = models[model_type.lower()]
    instance = model_class.objects.get(uuid=uuid_str)
    
    # Gestion spéciale pour les sessions (conversion hiérarchique)
    if model_type.lower() == 'session':
        markdown = model_to_markdown(instance.client, 1)
        if instance.programme:
            markdown += model_to_markdown(instance.programme, 2)
        markdown += model_to_markdown(instance, 3)
        
        # Conversion des séquences et breakouts
        for sequence in instance.sequences.filter(status='normal').order_by('order'):
            markdown += model_to_markdown(sequence, 4)
            for breakout in sequence.breakouts.filter(status='normal'):
                markdown += model_to_markdown(breakout, 5)
    else:
        markdown = model_to_markdown(instance)

    return markdown

def parse_markdown_section(text):
    """
    Analyse une section Markdown pour extraire les informations du modèle.
    
    Args:
        text: Texte Markdown à analyser
    
    Returns:
        dict: Informations extraites (type de modèle, UUID, champs)
    """
    # Extraction de l'en-tête avec le type de modèle et l'UUID
    header_match = re.search(r'\[@(\w+)::([\\w-]+)\]', text)
    if not header_match:
        return None

    model_type, uuid_str = header_match.groups()
    
    # Extraction des champs
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

def from_markdown(markdown_text):
    """
    Convertit un texte Markdown en objets Django.
    
    Args:
        markdown_text: Texte Markdown à convertir
    
    Returns:
        list: Objets Django créés ou mis à jour
    """
    # Dictionnaire de mappage des types de modèles
    models = {
        'client': Client,
        'programme': Programme,
        'session': Session,
        'sequence': Sequence,
        'breakout': BreakOut
    }

    # Séparation des sections Markdown
    sections = re.split(r'(?=^#+ \[@)', markdown_text, flags=re.MULTILINE)
    
    # Suivi des UUID traités pour chaque type de modèle
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
            
        # Analyse de chaque section
        parsed = parse_markdown_section(section)
        if not parsed or parsed['model_type'] not in models:
            continue

        model_class = models[parsed['model_type']]
        
        # Gestion des UUID nouveaux et existants
        if parsed['uuid'] != 'new':
            try:
                uuid_obj = uuid.UUID(parsed['uuid'])
                obj, created = model_class.objects.update_or_create(
                    uuid=uuid_obj,
                    defaults={
                        **parsed['fields'],
                        'status': 'normal'
                    }
                )
                processed_uuids[parsed['model_type']].add(uuid_obj)
            except ValueError:
                continue
        else:
            obj = model_class.objects.create(
                **parsed['fields'],
                uuid=uuid.uuid4(),
                status='normal'
            )
            processed_uuids[parsed['model_type']].add(obj.uuid)

        created_objects.append(obj)

    # Mise à jour du statut des objets non traités
    for model_type, uuids in processed_uuids.items():
        models[model_type].objects.filter(
            ~Q(uuid__in=uuids),
            status='normal'
        ).update(status='deleted')

    return created_objects