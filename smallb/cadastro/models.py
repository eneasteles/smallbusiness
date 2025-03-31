# MODELS.PY (em qualquer app do projeto, exemplo: core/models.py)

from django.db import models
from django.contrib.auth.models import User

# Perfil com celular vinculado ao User padrão
defaul_prefix = '+55'

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.celular})"


class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Lancamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True)
    data = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data} - {self.categoria}: R${self.valor}"