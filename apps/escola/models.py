from django.db import models

class Escola(models.Model):
    nome_escola = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['nome_escola']),
        ]

    def __str__(self):
        return self.nome_escola
