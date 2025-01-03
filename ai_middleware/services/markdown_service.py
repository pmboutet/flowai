import re
import uuid
from django.db.models import Q
from ..models import Client, Programme, Session, Sequence, BreakOut

# (Contenu précédent du fichier)

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