# API Markdown Import/Export

## Export Markdown

`GET /api/markdown/export/<model_type>/<uuid>/`

Exporte un objet et ses relations en format markdown.

### Paramètres URL

- `model_type`: Type d'objet (client, programme, session, sequence, breakout)
- `uuid`: UUID de l'objet

### Réponse

```json
{
    "markdown": "# [@Client::123e4567-e89b-12d3-a456-426614174000]\n**name**: Client Name\n..."
}
```

## Import Markdown

`POST /api/markdown/import/`

Crée ou met à jour des objets depuis un markdown.

### Corps de la requête

```json
{
    "markdown": "# [@Client::123e4567-e89b-12d3-a456-426614174000]\n**name**: Client Name\n..."
}
```

### Réponse

```json
{
    "message": "3 objects processed"
}
```

## Format Markdown

```markdown
# [@Client::uuid]
**name**: Nom du client
**context**: Contexte
**objectives**: Objectifs

## [@Programme::uuid]
**name**: Nom du programme
**description**: Description

### [@Session::uuid]
**title**: Titre de session
...

#### [@Sequence::uuid]
**title**: Titre de séquence
...

##### [@BreakOut::uuid]
**title**: Titre du breakout
...
```