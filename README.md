# FlowAI

FlowAI is a Django-based API platform that integrates various AI services including OpenAI, Anthropic Claude, and Mistral AI. It provides a comprehensive admin interface and RESTful API endpoints for managing AI conversations and workflows.

## Features

- REST API for AI interactions
- Admin interface using Django Unfold
- Google OAuth integration
- API documentation with Swagger/ReDoc
- Support for multiple AI providers (OpenAI, Anthropic, Mistral)
- Hierarchical data management with markdown import/export

## Documentation

- API Documentation: `https://your-domain/api/docs/` or locally at `https://127.0.0.1:8000/api/docs/`
- Alternative API Documentation: `https://your-domain/api/redoc/` or locally at `https://127.0.0.1:8000/api/redoc/`
- Admin Interface: `https://your-domain/admin/` or locally at `https://127.0.0.1:8000/admin/`

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pmboutet/flowai.git
cd flowai
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create a .env file):
```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
MISTRAL_API_KEY=your-mistral-key
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

## Development Server

Run the development server with HTTPS support:
```bash
python manage.py runsslserver
```

The application will be available at `https://127.0.0.1:8000/`

## Production Deployment

This application is configured for deployment on fly.io. To deploy:

1. Install flyctl:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login to fly.io:
```bash
flyctl auth login
```

3. Create the application:
```bash
flyctl apps create flowai
```

4. Create a volume for persistent data:
```bash
flyctl volumes create flowai_data --size 1
```

5. Set up environment variables:
```bash
flyctl secrets set DJANGO_SECRET_KEY="your-secret-key"
flyctl secrets set DJANGO_DEBUG="False"
flyctl secrets set ALLOWED_HOSTS=".fly.dev,your-domain.com"
# Add other necessary environment variables
```

6. Deploy:
```bash
flyctl deploy
```

## API Endpoints

- Conversations: `/api/conversations/`
- Clients: `/api/clients/`
- Programs: `/api/programmes/`
- Sessions: `/api/sessions/`
- Sequences: `/api/sequences/`
- Breakouts: `/api/breakouts/`

For detailed API documentation, visit the Swagger UI at `/api/docs/` or ReDoc at `/api/redoc/`

## Markdown Format

The API supports importing and exporting data in a specific markdown format that preserves hierarchical relationships between objects. The format is structured as follows:

### Basic Format
```markdown
# [@Type::UUID] **field1**: value1 **field2**: value2
```

Each line represents one object with:
- Hierarchy level indicated by number of `#`
- Object type and UUID in `[@Type::UUID]` format
- Fields as `**fieldname**: value` pairs

### Example
```markdown
# [@Client::550e8400-e29b-41d4-a716-446655440000] **name**: ACME Corp **context**: Global company
## [@Programme::663e8400-e29b-41d4-a716-446655440123] **name**: Sales Training
### [@Session::774e8400-e29b-41d4-a716-446655440456] **title**: Introduction
```

### Available Fields
- Client: name, context, objectives
- Programme: name, description
- Session: title, context, objectives, inputs, outputs, participants, design_principles, deliverables
- Sequence: title, objective, input_text, output_text, order
- BreakOut: title, description, objective

For creating new objects, use `new` as the UUID: `[@Type::new]`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details