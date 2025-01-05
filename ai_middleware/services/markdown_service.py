import re
import uuid
from django.db.models import Q
from ..models import Client, Programme, Session, Sequence, BreakOut

def to_markdown(obj, export_related=True, level=1, initial_level=1):
    """
    Convertit un objet en format Markdown sur une seule ligne avec ses parents et enfants.
    Format: # [@Type::UUID] **champ**: valeur **champ2**: valeur2
    
    Args:
        obj: Instance de modèle Django à convertir
        export_related (bool): Si True, exporte aussi les objets liés
        level (int): Niveau de titre Markdown actuel
        initial_level (int): Niveau de départ pour calculer les niveaux parents/enfants
    
    Returns:
        str: Représentation Markdown de l'objet, ses parents et ses enfants
    """
    model_name = obj.__class__.__name__
    markdown = ""
    
    # Si ce n'est pas l'objet initial, adapter le niveau
    is_parent = level < initial_level
    
    # Générer les parents d'abord si c'est l'objet initial
    if level == initial_level:
        # Pour une session, exporter le client et le programme parents
        if isinstance(obj, Session):
            if obj.client:
                markdown += to_markdown(obj.client, level=1, initial_level=initial_level)
            if obj.programme:
                markdown += to_markdown(obj.programme, level=2, initial_level=initial_level)
        # Pour une séquence, exporter la session, le programme et le client parents
        elif isinstance(obj, Sequence):
            if obj.session and obj.session.client:
                markdown += to_markdown(obj.session.client, level=1, initial_level=initial_level)
            if obj.session and obj.session.programme:
                markdown += to_markdown(obj.session.programme, level=2, initial_level=initial_level)
            if obj.session:
                markdown += to_markdown(obj.session, level=3, initial_level=initial_level)
        # Pour un breakout, exporter la sequence et ses parents
        elif isinstance(obj, BreakOut):
            if obj.sequence and obj.sequence.session and obj.sequence.session.client:
                markdown += to_markdown(obj.sequence.session.client, level=1, initial_level=initial_level)
            if obj.sequence and obj.sequence.session and obj.sequence.session.programme:
                markdown += to_markdown(obj.sequence.session.programme, level=2, initial_level=initial_level)
            if obj.sequence and obj.sequence.session:
                markdown += to_markdown(obj.sequence.session, level=3, initial_level=initial_level)
            if obj.sequence:
                markdown += to_markdown(obj.sequence, level=4, initial_level=initial_level)
    
    # Générer la ligne pour l'objet actuel
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
    
    markdown += line.strip() + '\n'
    
    # Gérer les enfants si c'est l'objet initial ou un parent
    if level >= initial_level:
        if isinstance(obj, Client):
            for prog in Programme.objects.filter(client=obj):
                markdown += to_markdown(prog, level=level+1, initial_level=initial_level)
        elif isinstance(obj, Programme):
            for session in Session.objects.filter(programme=obj):
                markdown += to_markdown(session, level=level+1, initial_level=initial_level)
        elif isinstance(obj, Session):
            for sequence in Sequence.objects.filter(session=obj).order_by('order'):
                markdown += to_markdown(sequence, level=level+1, initial_level=initial_level)
        elif isinstance(obj, Sequence):
            for breakout in BreakOut.objects.filter(sequence=obj):
                markdown += to_markdown(breakout, level=level+1, initial_level=initial_level)
    
    return markdown

# Le reste du fichier reste identique
