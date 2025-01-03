from django.db import migrations, models
import uuid

def gen_uuid():
    return uuid.uuid4()

class Migration(migrations.Migration):
    dependencies = [
        ('ai_middleware', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='uuid',
            field=models.UUIDField(default=gen_uuid, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='programme',
            name='uuid',
            field=models.UUIDField(default=gen_uuid, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='session',
            name='uuid',
            field=models.UUIDField(default=gen_uuid, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='sequence',
            name='uuid',
            field=models.UUIDField(default=gen_uuid, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='breakout',
            name='uuid',
            field=models.UUIDField(default=gen_uuid, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='uuid',
            field=models.UUIDField(default=gen_uuid, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='client',
            name='status',
            field=models.CharField(choices=[("normal", "Normal"), ("deleted", "Deleted"), ("archived", "Archived")], default="normal", max_length=10),
        ),
        migrations.AddField(
            model_name='programme',
            name='status',
            field=models.CharField(choices=[("normal", "Normal"), ("deleted", "Deleted"), ("archived", "Archived")], default="normal", max_length=10),
        ),
        migrations.AddField(
            model_name='session',
            name='status',
            field=models.CharField(choices=[("normal", "Normal"), ("deleted", "Deleted"), ("archived", "Archived")], default="normal", max_length=10),
        ),
        migrations.AddField(
            model_name='sequence',
            name='status',
            field=models.CharField(choices=[("normal", "Normal"), ("deleted", "Deleted"), ("archived", "Archived")], default="normal", max_length=10),
        ),
        migrations.AddField(
            model_name='breakout',
            name='status',
            field=models.CharField(choices=[("normal", "Normal"), ("deleted", "Deleted"), ("archived", "Archived")], default="normal", max_length=10),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='status',
            field=models.CharField(choices=[("normal", "Normal"), ("deleted", "Deleted"), ("archived", "Archived")], default="normal", max_length=10),
        ),
    ]