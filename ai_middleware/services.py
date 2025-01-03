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

def to_markdown(uuid, model_type):
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
    instance = model_class.objects.get(uuid=uuid)
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
