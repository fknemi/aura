from django.db import models
from pgvector.django import VectorField, HnswIndex
from django.contrib.auth import get_user_model

User = get_user_model()


class Website(models.Model):
    url             = models.URLField(max_length=2048, unique=True)
    domain          = models.CharField(max_length=255, blank=True, db_index=True) 
    title           = models.CharField(max_length=512, blank=True)
    favicon_url     = models.URLField(max_length=2048, blank=True)

    raw_html        = models.TextField(blank=True)
    content         = models.TextField(blank=True)  
    summary         = models.TextField(blank=True)  
    language        = models.CharField(max_length=16, blank=True)

    meta_description = models.TextField(blank=True)
    meta_keywords    = models.TextField(blank=True)
    og_image_url     = models.URLField(max_length=2048, blank=True)

    status_code     = models.PositiveSmallIntegerField(null=True, blank=True)
    content_type    = models.CharField(max_length=128, blank=True) 
    content_length  = models.PositiveIntegerField(null=True, blank=True) 

    added_by        = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="websites",
    )
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    expires_at      = models.DateTimeField(null=True, blank=True)

    # --- pgvector embedding ---
    # 1536 = OpenAI text-embedding-3-small
    # Swap for 768 / 512 etc. to match your model
    embedding       = VectorField(dimensions=1536, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            HnswIndex(
                name="website_embedding_hnsw_idx",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            ),
        ]

    def __str__(self) -> str:
        return str(self.title) or str(self.url)

