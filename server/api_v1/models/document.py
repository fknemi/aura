from django.db import models
from pgvector.django import VectorField, HnswIndex
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):

    class DocumentType(models.TextChoices):
        PDF  = "pdf",  "PDF"
        TXT  = "txt",  "Plain Text"
        DOCX = "docx", "Word Document"
        CSV  = "csv",  "CSV"
        MD   = "md",   "Markdown"
        HTML = "html", "HTML"
        OTHER = "other", "Other"

    title       = models.CharField(max_length=255, blank=True)
    file        = models.FileField(upload_to="documents/%Y/%m/%d/")   
    file_url    = models.URLField(blank=True)
    mime_type   = models.CharField(max_length=128, blank=True)
    file_size   = models.PositiveIntegerField(null=True, blank=True) 
    doc_type    = models.CharField(                                 
        max_length=16,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        db_index=True,
    )
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="documents",        
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    expires_at  = models.DateTimeField(null=True, blank=True)

    # --- pgvector embedding ---
    # 1536 = OpenAI text-embedding-3-small
    # Swap for 768 / 512 etc. to match your model
    embedding   = VectorField(dimensions=1536, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            HnswIndex(
                name="doc_embedding_hnsw_idx", 
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]

    def __str__(self) -> str:
        return str(self.title) if self.title else f"Document {self.pk}"
