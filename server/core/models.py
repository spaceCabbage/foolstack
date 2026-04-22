from django.db import models
from core.utils import generate_unique_id

class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for all models.
    """
    id = models.CharField(
        max_length=26,
        primary_key=True,
        default=generate_unique_id,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
