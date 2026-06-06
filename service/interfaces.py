from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from domain.figurinha import FigurinhaOut


@dataclass
class CreateFigurinhaData:
    numero: str
    nome: str
    selecao: str
    tipo: str
    posicao: str
    created_at: datetime
    updated_at: datetime


@dataclass
class UpdateFigurinhaData:
    numero: str
    nome: str
    selecao: str
    tipo: str
    posicao: str
    updated_at: datetime


class FigurinhaNotFound(Exception):
    pass


class MissingFields(Exception):
    pass


class InvalidTipo(Exception):
    pass


class InvalidPosicao(Exception):
    pass


class FigurinhaRepository(ABC):
    @abstractmethod
    def create(self, data: CreateFigurinhaData) -> dict:
        pass

    @abstractmethod
    def find_all(self) -> list[dict]:
        pass

    @abstractmethod
    def find_all_by_posicao(self, data: dict) -> list[dict]:
        pass

    @abstractmethod
    def find_all_by_tipo(self, data: dict) -> list[dict]:
        pass

    @abstractmethod
    def find_all_by_posicao_and_tipo(self, data: dict) -> list[dict]:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> dict | None:
        pass

    @abstractmethod
    def update(self, id: int, data: UpdateFigurinhaData) -> dict | None:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class FigurinhaService(ABC):
    @abstractmethod
    def create(self, data: dict) -> FigurinhaOut:
        pass

    @abstractmethod
    def list(self, posicao: str | None = None, tipo: str | None = None) -> list[FigurinhaOut]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> FigurinhaOut:
        pass

    @abstractmethod
    def update(self, id: int, data: dict) -> FigurinhaOut:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
