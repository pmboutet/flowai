from django.db import models
import uuid

class Client(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    context = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Programme(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Session(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    context = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    inputs = models.TextField(blank=True)
    outputs = models.TextField(blank=True)
    participants = models.TextField(blank=True)
    design_principles = models.TextField(blank=True)
    deliverables = models.TextField(blank=True)
    
    def __str__(self):
        return self.title

class Sequence(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    objective = models.TextField(blank=True)
    input_text = models.TextField(blank=True)
    output_text = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class BreakOut(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    
    def __str__(self):
        return self.title