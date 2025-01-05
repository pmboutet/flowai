import re
import uuid
from django.db.models import Q
from ..models import Client, Programme, Session, Sequence, BreakOut

def to_markdown(obj, export_related=True, level=1):
    """
    Convertit un objet en format Markdown avec métadonnées.
    
    Args:
        obj: Instance de modèle Django à convertir
        export_related (bool): Si True, exporte aussi les objets liés
        level (int): Niveau de titre Markdown
    
    Returns:
        str: Représentation Markdown de l'objet
    """
    model_name = obj.__class__.__name__
    hashes = '#' * level
    title = f'{hashes} [@{model_name}::{str(obj.uuid)}]\n\n'
    
    # Filtrer les champs à exporter
    excluded_fields = ['id', 'created_at', 'updated_at', 'uuid']
    fields = [f for f in obj.__class__._meta.get_fields() 
             if not f.is_relation and f.name not in excluded_fields]
    
    # Générer le contenu des champs
    content = ''
    for field in fields:
        value = getattr(obj, field.name)
        if value is not None:
            # Gérer les UUIDs spécialement
            if isinstance(value, uuid.UUID):
                value = str(value)
            content += f'**{field.name}**: {value}\n'
    
    # Ajouter les clés étrangères importantes
    if isinstance(obj, Programme):
        content += f'**client_uuid**: {str(obj.client.uuid)}\n'
    elif isinstance(obj, Session):
        content += f'**client_uuid**: {str(obj.client.uuid)}\n'
        if obj.programme:
            content += f'**programme_uuid**: {str(obj.programme.uuid)}\n'
    elif isinstance(obj, Sequence):
        content += f'**session_uuid**: {str(obj.session.uuid)}\n'
    elif isinstance(obj, BreakOut):
        content += f'**sequence_uuid**: {str(obj.sequence.uuid)}\n'
    
    markdown = title + content + '\n'
    
    # Gérer les relations si demandé
    if export_related:
        if isinstance(obj, Client):
            programmes = Programme.objects.filter(client=obj)
            for prog in programmes:
                markdown += to_markdown(prog, level=level+1)
                
        elif isinstance(obj, Programme):
            sessions = Session.objects.filter(programme=obj)
            for session in sessions:
                markdown += to_markdown(session, level=level+1)
                
        elif isinstance(obj, Session):
            sequences = Sequence.objects.filter(session=obj).order_by('order')
            for sequence in sequences:
                markdown += to_markdown(sequence, level=level+1)
                
        elif isinstance(obj, Sequence):
            breakouts = BreakOut.objects.filter(sequence=obj)
            for breakout in breakouts:
                markdown += to_markdown(breakout, level=level+1)
    
    return markdown

def from_markdown(markdown_text):
    """
    Crée ou met à jour des objets à partir d'un texte Markdown.
    
    Args:
        markdown_text (str): Texte Markdown à convertir
    
    Returns:
        list: Liste des objets créés ou mis à jour
    """
    objects = []
    sections = re.split(r'(?=^#+ \[@)', markdown_text, flags=re.MULTILINE)
    
    for section in sections:
        if not section.strip():
            continue
            
        # Extraire les métadonnées
        header_match = re.match(r'#+\s+\[@(\w+)::([^\]]+)\]', section)
        if not header_match:
            continue
            
        model_name, obj_uuid = header_match.groups()
        model_class = globals().get(model_name)
        
        if not model_class:
            continue
            
        # Extraire les champs et valeurs
        fields = {}
        foreign_keys = {}
        for line in section.split('\n'):
            field_match = re.match(r'\*\*(\w+)\*\*:\s*(.+)', line)
            if field_match:
                field_name, value = field_match.groups()
                # Gérer les clés étrangères séparément
                if field_name.endswith('_uuid'):
                    related_model_name = field_name.replace('_uuid', '')
                    if related_model_name == 'programme':
                        foreign_keys['programme'] = value.strip()
                    elif related_model_name == 'client':
                        foreign_keys['client'] = value.strip()
                    elif related_model_name == 'session':
                        foreign_keys['session'] = value.strip()
                    elif related_model_name == 'sequence':
                        foreign_keys['sequence'] = value.strip()
                else:
                    fields[field_name] = value.strip()
        
        # Résoudre les clés étrangères
        for field_name, uuid_value in foreign_keys.items():
            try:
                uuid_obj = uuid.UUID(uuid_value)
                if field_name == 'programme':
                    fields['programme'] = Programme.objects.get(uuid=uuid_obj)
                elif field_name == 'client':
                    fields['client'] = Client.objects.get(uuid=uuid_obj)
                elif field_name == 'session':
                    fields['session'] = Session.objects.get(uuid=uuid_obj)
                elif field_name == 'sequence':
                    fields['sequence'] = Sequence.objects.get(uuid=uuid_obj)
            except (ValueError, Programme.DoesNotExist, Client.DoesNotExist,
                    Session.DoesNotExist, Sequence.DoesNotExist):
                continue
        
        # Créer ou mettre à jour l'objet
        if obj_uuid.lower() == 'new':
            # Générer un nouvel UUID
            fields['uuid'] = uuid.uuid4()
            obj = model_class.objects.create(**fields)
        else:
            try:
                # Convertir l'UUID du titre
                uuid_obj = uuid.UUID(obj_uuid)
                obj = model_class.objects.filter(uuid=uuid_obj).first()
                
                if obj:
                    # Mise à jour des champs excepté l'UUID
                    for field, value in fields.items():
                        if field != 'uuid':
                            setattr(obj, field, value)
                    obj.save()
                else:
                    # Créer un nouvel objet avec l'UUID spécifié
                    fields['uuid'] = uuid_obj
                    obj = model_class.objects.create(**fields)
            except ValueError:
                continue
        
        objects.append(obj)
    
    return objects

def create_objects_from_markdown(markdown_text):
    """
    Crée des objets à partir d'un texte Markdown en respectant l'ordre hiérarchique.
    
    Args:
        markdown_text (str): Texte Markdown à convertir
    
    Returns:
        dict: Dictionnaire des objets créés
    """
    # Création des objets dans l'ordre
    created_objects = {}
    
    # Étape 1: Créer le client
    client_sections = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Client::new]' in s]
    if not client_sections:
        raise ValueError("No client section found in markdown text")
    client = from_markdown(client_sections[0])[0]
    created_objects['client'] = client
    
    # Étape 2: Créer le programme avec l'UUID du client
    programme_sections = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Programme::new]' in s]
    if programme_sections:
        programme_section = programme_sections[0]
        programme_section = programme_section.replace('[@Programme::new]', 
            f'[@Programme::new]\n**client_uuid**: {str(client.uuid)}')
        programme = from_markdown(programme_section)[0]
        created_objects['programme'] = programme
    
        # Étape 3: Créer la session avec l'UUID du client et du programme
        session_sections = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Session::new]' in s]
        if session_sections:
            session_section = session_sections[0]
            session_section = session_section.replace('[@Session::new]', 
                f'[@Session::new]\n**client_uuid**: {str(client.uuid)}\n**programme_uuid**: {str(programme.uuid)}')
            session = from_markdown(session_section)[0]
            created_objects['session'] = session
    
            # Étape 4: Créer les séquences avec l'UUID de la session
            sequence_sections = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Sequence::new]' in s]
            sequences = []
            for i, seq_section in enumerate(sequence_sections):
                seq_section = seq_section.replace('[@Sequence::new]', 
                    f'[@Sequence::new]\n**session_uuid**: {str(session.uuid)}\n**order**: {i+1}')
                sequence = from_markdown(seq_section)[0]
                sequences.append(sequence)
            created_objects['sequences'] = sequences
    
            # Étape 5: Créer les breakouts avec l'UUID de la séquence
            breakout_sections = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@BreakOut::new]' in s]
            breakouts = []
            for i, breakout_section in enumerate(breakout_sections):
                current_sequence = sequences[i // 2]
                breakout_section = breakout_section.replace('[@BreakOut::new]', 
                    f'[@BreakOut::new]\n**sequence_uuid**: {str(current_sequence.uuid)}')
                breakout = from_markdown(breakout_section)[0]
                breakouts.append(breakout)
            created_objects['breakouts'] = breakouts
    
    return created_objects