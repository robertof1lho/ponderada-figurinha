from datetime import datetime
from pydantic import BaseModel
from domain.figurinha import Tipo, Posicao


class FigurinhaCreate(BaseModel):
    numero: str
    nome: str
    selecao: str
    tipo: Tipo
    posicao: Posicao


class FigurinhaUpdate(BaseModel):
    numero: str
    nome: str
    selecao: str
    tipo: Tipo
    posicao: Posicao


class FigurinhaOut(BaseModel):
    id: int
    numero: str
    nome: str
    selecao: str
    tipo: Tipo
    posicao: Posicao
    created_at: datetime
    updated_at: datetime
