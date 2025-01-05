import re
import uuid
from django.db.models import Q
from ..models import Client, Programme, Session, Sequence, BreakOut

def to_markdown(obj, export_related=True, level=1):
    """
    Convertit un objet en format Markdown sur une seule ligne avec des niveaux de hiérarchie.
    Format: # [@Type::UUID] **champ**: valeur **champ2**: valeur2
    
    Args:
        obj: Instance de modèle Django à convertir
        export_related (bool): Si True, exporte aussi les objets liés
        level (int): Niveau de titre Markdown (nombre de #)
    
    Returns:
        str: Représentation Markdown de l'objet et ses relations
    """
    model_name = obj.__class__.__name__
    hashes = '#' * level
    line = f"{hashes} [@{model_name}::{str(obj.uuid)}] "
    
    # Définir les champs à exporter pour chaque type de modèle
    if isinstance(obj, Client):
        fields = ['name', 'context', 'objectives']
    elif isinstance(obj, Programme):
        fields = ['name', 'description']
    elif isinstance(obj, Session):
        fields = ['title', 'context', 'objectives', 'inputs', 'outputs',
                 'participants', 'design_principles', 'deliverables']
    elif isinstance(obj, Sequence):
        fields = ['title', 'objective', 'input_text', 'output_text', 'order']
    elif isinstance(obj, BreakOut):
        fields = ['title', 'description', 'objective']
    else:
        fields = []
    
    # Générer le contenu des champs sur la même ligne
    for field in fields:
        value = getattr(obj, field, None)
        if value is not None:
            # Nettoyer et formater la valeur
            value = str(value).replace('\n', ' ').replace('\r', ' ')
            value = re.sub(r'\s+', ' ', value).strip()
            line += f"**{field}**: {value} "
    
    markdown = line.strip() + '\n'
    
    # Gérer les relations
    if export_related:
        if isinstance(obj, Client):
            for prog in Programme.objects.filter(client=obj):
                markdown += to_markdown(prog, level=level+1)
                
            for session in Session.objects.filter(client=obj, programme__isnull=True):
                markdown += to_markdown(session, level=level+2)
                
        elif isinstance(obj, Programme):
            for session in Session.objects.filter(programme=obj):
                markdown += to_markdown(session, level=level+1)
                
        elif isinstance(obj, Session):
            for sequence in Sequence.objects.filter(session=obj).order_by('order'):
                markdown += to_markdown(sequence, level=level+1)
                
        elif isinstance(obj, Sequence):
            for breakout in BreakOut.objects.filter(sequence=obj):
                markdown += to_markdown(breakout, level=level+1)
    
    return markdown

def from_markdown(markdown_text):
    """
    Crée ou met à jour des objets à partir d'un texte Markdown.
    Format attendu: # [@Type::UUID] **champ**: valeur **champ2**: valeur2
    
    Args:
        markdown_text (str): Texte Markdown à convertir
    
    Returns:
        list: Liste des objets créés ou mis à jour
    """
    objects = []
    lines = markdown_text.strip().split('\n')
    
    for line in lines:
        if not line.strip():
            continue
            
        # Extraire le type et l'UUID
        header_match = re.match(r'#+\s+\[@(\w+)::([^\]]+)\]\s*(.+)?', line)
        if not header_match:
            continue
            
        model_name, obj_uuid, fields_text = header_match.groups()
        model_class = globals().get(model_name)
        
        if not model_class or not fields_text:
            continue
            
        # Extraire les champs et valeurs
        fields = {}
        field_matches = re.finditer(r'\*\*(\w+)\*\*:\s*([^*]+?)(?=\s+\*\*|$)', fields_text)
        
        for match in field_matches:
            field_name, value = match.groups()
            fields[field_name] = value.strip()
        
        # Créer ou mettre à jour l'objet
        if obj_uuid.lower() == 'new':
            # Générer un nouvel UUID
            fields['uuid'] = uuid.uuid4()
            obj = model_class.objects.create(**fields)
        else:
            try:
                # Convertir l'UUID
                uuid_obj = uuid.UUID(obj_uuid)
                obj = model_class.objects.filter(uuid=uuid_obj).first()
                
                if obj:
                    # Mettre à jour les champs
                    for field, value in fields.items():
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
    lines = markdown_text.strip().split('\n')
    created_objects = {}
    
    # Identifier les lignes par type
    client_line = next((l for l in lines if '[@Client::' in l), None)
    programme_line = next((l for l in lines if '[@Programme::' in l), None)
    session_line = next((l for l in lines if '[@Session::' in l), None)
    sequence_lines = [l for l in lines if '[@Sequence::' in l]
    breakout_lines = [l for l in lines if '[@BreakOut::' in l]
    
    # Créer les objets dans l'ordre
    if client_line:
        client = from_markdown(client_line)[0]
        created_objects['client'] = client
        
        if programme_line:
            # Ajouter la référence au client
            programme_line = programme_line.strip() + f" **client_id**: {str(client.uuid)}"
            programme = from_markdown(programme_line)[0]
            created_objects['programme'] = programme
            
            if session_line:
                # Ajouter les références au client et au programme
                session_line = session_line.strip() + f" **client_id**: {str(client.uuid)} **programme_id**: {str(programme.uuid)}"
                session = from_markdown(session_line)[0]
                created_objects['session'] = session
                
                # Créer les séquences
                sequences = []
                for i, seq_line in enumerate(sequence_lines):
                    seq_line = seq_line.strip() + f" **session_id**: {str(session.uuid)} **order**: {i+1}"
                    sequence = from_markdown(seq_line)[0]
                    sequences.append(sequence)
                created_objects['sequences'] = sequences
                
                # Créer les breakouts
                breakouts = []
                for i, break_line in enumerate(breakout_lines):
                    sequence = sequences[i // 2]
                    break_line = break_line.strip() + f" **sequence_id**: {str(sequence.uuid)}"
                    breakout = from_markdown(break_line)[0]
                    breakouts.append(breakout)
                created_objects['breakouts'] = breakouts
    
    return created_objects