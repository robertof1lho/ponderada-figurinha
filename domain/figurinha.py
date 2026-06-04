from enum import Enum


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


class FigurinhaNotFound(Exception):
    pass


class MissingFields(Exception):
    pass


class InvalidTipo(Exception):
    pass


class InvalidPosicao(Exception):
    pass
