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
    title = f'{"#" * level} [@{model_name}::{obj.id}]\n\n'
    
    # Filtrer les champs à exporter
    excluded_fields = ['id', 'created_at', 'updated_at']
    fields = [f for f in obj.__class__._meta.get_fields() 
             if not f.is_relation and f.name not in excluded_fields]
    
    # Générer le contenu des champs
    content = ''
    for field in fields:
        value = getattr(obj, field.name)
        if value is not None:
            content += f'**{field.name}**: {value}\n'
    
    markdown = title + content + '\n'
    
    # Gérer les relations si demandé
    if export_related:
        if isinstance(obj, Client):
            # Exporter les programmes du client
            programmes = Programme.objects.filter(client=obj)
            for prog in programmes:
                markdown += to_markdown(prog, level=level+1)
                
        elif isinstance(obj, Programme):
            # Exporter les sessions du programme
            sessions = Session.objects.filter(programme=obj)
            for session in sessions:
                markdown += to_markdown(session, level=level+1)
                
        elif isinstance(obj, Session):
            # Exporter les séquences de la session
            sequences = Sequence.objects.filter(session=obj).order_by('order')
            for sequence in sequences:
                markdown += to_markdown(sequence, level=level+1)
                
        elif isinstance(obj, Sequence):
            # Exporter les breakouts de la séquence
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
            
        model_name, obj_id = header_match.groups()
        model_class = globals().get(model_name)
        
        if not model_class:
            continue
            
        # Extraire les champs et valeurs
        fields = {}
        for line in section.split('\n'):
            field_match = re.match(r'\*\*(\w+)\*\*:\s*(.+)', line)
            if field_match:
                field_name, value = field_match.groups()
                fields[field_name] = value.strip()
        
        # Créer ou mettre à jour l'objet
        if obj_id.lower() == 'new':
            # Générer un nouvel UUID
            fields['id'] = uuid.uuid4()
            obj = model_class.objects.create(**fields)
        else:
            # Mettre à jour l'objet existant
            obj = model_class.objects.filter(Q(id=obj_id) | Q(uuid=obj_id)).first()
            if obj:
                for field, value in fields.items():
                    setattr(obj, field, value)
                obj.save()
            else:
                # Si l'objet n'existe pas, le créer avec l'ID spécifié
                fields['id'] = obj_id
                obj = model_class.objects.create(**fields)
        
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
    client_section = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Client::new]' in s][0]
    client = from_markdown(client_section)[0]
    created_objects['client'] = client
    
    # Étape 2: Créer le programme avec l'ID du client
    programme_section = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Programme::new]' in s][0]
    programme_section = programme_section.replace('[@Programme::new]', f'[@Programme::new]\n**client_id**: {client.id}')
    programme = from_markdown(programme_section)[0]
    created_objects['programme'] = programme
    
    # Étape 3: Créer la session avec l'ID du client et du programme
    session_section = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Session::new]' in s][0]
    session_section = session_section.replace('[@Session::new]', 
        f'[@Session::new]\n**client_id**: {client.id}\n**programme_id**: {programme.id}')
    session = from_markdown(session_section)[0]
    created_objects['session'] = session
    
    # Étape 4: Créer les séquences avec l'ID de la session
    sequence_sections = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@Sequence::new]' in s]
    sequences = []
    for i, seq_section in enumerate(sequence_sections):
        seq_section = seq_section.replace('[@Sequence::new]', 
            f'[@Sequence::new]\n**session_id**: {session.id}\n**order**: {i+1}')
        sequence = from_markdown(seq_section)[0]
        sequences.append(sequence)
    created_objects['sequences'] = sequences
    
    # Étape 5: Créer les breakouts avec l'ID de la séquence
    breakout_sections = [s for s in re.split(r'(?=^#+ \[@)', markdown_text) if '[@BreakOut::new]' in s]
    breakouts = []
    for i, breakout_section in enumerate(breakout_sections):
        # Associer au breakout à la séquence appropriée
        current_sequence = sequences[i // 2]
        breakout_section = breakout_section.replace('[@BreakOut::new]', 
            f'[@BreakOut::new]\n**sequence_id**: {current_sequence.id}')
        breakout = from_markdown(breakout_section)[0]
        breakouts.append(breakout)
    created_objects['breakouts'] = breakouts
    
    return created_objects