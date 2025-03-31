# smallbusiness
Gerenciador Financeiro para Pequenos Negócios

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# ------------------------------
# Usuário customizado baseado em celular
# ------------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, celular, password=None, **extra_fields):
        if not celular:
            raise ValueError("O celular é obrigatório")
        user = self.model(celular=celular, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, celular, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(celular, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    celular = models.CharField(max_length=15, unique=True)  # Ex: +5581999999999
    nome = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'celular'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    def __str__(self):
        return self.nome

# ------------------------------
# Categoria de transações
# ------------------------------
class Categoria(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

# ------------------------------
# Lançamentos financeiros
# ------------------------------
class Lancamento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True)
    data = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data} - {self.categoria}: R${self.valor}"

