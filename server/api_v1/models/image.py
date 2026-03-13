from django.db import models
from pgvector.django import VectorField, HnswIndex
from django.contrib.auth import get_user_model

User = get_user_model()


class Image(models.Model):
    title       = models.CharField(max_length=255, blank=True)
    file        = models.ImageField(upload_to="images/%Y/%m/%d/")
    file_url    = models.URLField(blank=True)       
    mime_type   = models.CharField(max_length=64, blank=True) 
    file_size   = models.PositiveIntegerField(null=True, blank=True)

    description = models.TextField(blank=True)  
    uploaded_by = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="images",
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    expires_at  = models.DateTimeField(null=True, blank=True)

    # --- pgvector embedding ---
    # 1536 = OpenAI text-embedding-3-small / CLIP ViT-L/14
    # Swap for 768 (CLIP ViT-B/32), 512, etc. to match your model
    embedding   = VectorField(dimensions=1536, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            HnswIndex(
                name="image_embedding_hnsw_idx",
                fields=["embedding"],
                m=16,             
                ef_construction=64, 
                opclasses=["vector_cosine_ops"],
            )
        ]

    def __str__(self) -> str:
        return str(self.title) if self.title else f"Image {self.pk}"


