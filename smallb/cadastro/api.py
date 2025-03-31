# API.PY (no mesmo app que models.py)

from ninja import NinjaAPI, Schema
from typing import List
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Categoria, Lancamento, Perfil
from django.contrib.auth.models import User
from datetime import date
from ninja.security import HttpBearer

api = NinjaAPI()

# Schemas
class AuthInput(Schema):
    celular: str
    senha: str

class CategoriaIn(Schema):
    nome: str
    tipo: str

class CategoriaOut(Schema):
    id: int
    nome: str
    tipo: str

class LancamentoIn(Schema):
    categoria_id: int
    valor: float
    descricao: str
    data: date

class LancamentoOut(Schema):
    id: int
    categoria: str
    valor: float
    descricao: str
    data: date

# Autenticação com Token
class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

auth = TokenAuth()

# LOGIN - retorna token
@api.post("/login")
def login(request, data: AuthInput):
    try:
        perfil = Perfil.objects.get(celular=data.celular)
        user = authenticate(username=perfil.user.username, password=data.senha)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return {"token": token.key}
        return {"error": "Senha incorreta"}
    except Perfil.DoesNotExist:
        return {"error": "Celular não cadastrado"}

# CRUD de categorias
@api.get("/categorias", response=List[CategoriaOut], auth=auth)
def listar_categorias(request):
    return Categoria.objects.filter(usuario=request.auth)

@api.post("/categorias", response=CategoriaOut, auth=auth)
def criar_categoria(request, data: CategoriaIn):
    cat = Categoria.objects.create(usuario=request.auth, **data.dict())
    return cat

# Criar lançamentos
@api.post("/lancamentos", response=LancamentoOut, auth=auth)
def criar_lancamento(request, data: LancamentoIn):
    categoria = Categoria.objects.get(id=data.categoria_id, usuario=request.auth)
    lanc = Lancamento.objects.create(
        usuario=request.auth,
        categoria=categoria,
        valor=data.valor,
        descricao=data.descricao,
        data=data.data,
    )
    return LancamentoOut(
        id=lanc.id,
        categoria=categoria.nome,
        valor=lanc.valor,
        descricao=lanc.descricao,
        data=lanc.data
    )

