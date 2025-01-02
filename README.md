# FlowAI

Middleware Django utilisant Django Rest Framework pour interagir avec l'API ChatGPT.

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/pmboutet/flowai.git
cd flowai
```

2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
- Copier `.env.example` vers `.env`
- Remplir les variables dans `.env` avec vos clés

5. Appliquer les migrations :
```bash
python manage.py migrate
```

6. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

7. Lancer le serveur :
```bash
python manage.py runserver
```

## Utilisation

L'API expose un endpoint `/api/conversations/` qui accepte :

- GET : Liste toutes les conversations
- POST : Crée une nouvelle conversation avec ChatGPT

Exemple de requête POST :
```json
{
    "user_input": "Quelle est la capitale de la France ?"
}
```

### Authentication

L'API nécessite une authentification. Utilisez les identifiants du superutilisateur créé précédemment.

## Structure du projet

- `ai_middleware/` : Application principale
  - `models.py` : Définition du modèle Conversation
  - `serializers.py` : Sérialiseur pour l'API
  - `views.py` : Vue gérant les interactions avec ChatGPT
  - `urls.py` : Configuration des URLs

- `flowai/` : Configuration du projet
  - `settings.py` : Paramètres du projet
  - `urls.py` : URLs principales

## Sécurité

- Toutes les requêtes nécessitent une authentification
- Les clés API sont gérées via des variables d'environnement
- L'historique des conversations est sauvegardé en base de données