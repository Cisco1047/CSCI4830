from django.db import models

# Create your models here.
from django.db import models


class TaskForConfiguration(models.Model):
    # ...
    instructions = models.JSONField(default=dict, blank=True)  # JSON schema shown below
