from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('ai_middleware', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='provider',
            field=models.CharField(
                choices=[
                    ('grok', 'Grok'),
                    ('openai', 'OpenAI'),
                    ('claude', 'Claude'),
                    ('mistral', 'Mistral')
                ],
                default='grok',
                max_length=10
            ),
        ),
    ]