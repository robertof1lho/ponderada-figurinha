from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class Tipo(str, Enum):
    comum = "comum"
    brilhante = "brilhante"
    legends_ouro = "legends_ouro"
    legends_bronze = "legends_bronze"


class Posicao(str, Enum):
    goleiro = "Goleiro"
    zagueiro = "Zagueiro"
    meio_campista = "Meio-campista"
    atacante = "Atacante"


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
