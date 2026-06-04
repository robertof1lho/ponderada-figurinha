from datetime import datetime
from pydantic import ValidationError
from service.interfaces import FigurinhaRepository, FigurinhaService, CreateFigurinhaData, UpdateFigurinhaData
from domain.schemas import FigurinhaCreate, FigurinhaUpdate, FigurinhaOut
from domain.figurinha import MissingFields, InvalidTipo, InvalidPosicao


class FigurinhaServiceImpl(FigurinhaService):
    def __init__(self, repo: FigurinhaRepository):
        self.repo = repo

    def _validate_create(self, data: FigurinhaCreate) -> FigurinhaCreate:
        try:
            return FigurinhaCreate(**data.model_dump())
        except ValidationError as e:
            for error in e.errors():
                field = error["loc"][0]
                kind  = error["type"]
                if kind == "missing":
                    raise MissingFields(f"campo obrigatório ausente: {field}")
                if field == "tipo":
                    raise InvalidTipo(f"tipo inválido: {data.tipo}")
                if field == "posicao":
                    raise InvalidPosicao(f"posicao inválida: {data.posicao}")
            raise MissingFields("dados inválidos")

    def _validate_update(self, data: FigurinhaUpdate) -> FigurinhaUpdate:
        try:
            return FigurinhaUpdate(**data.model_dump())
        except ValidationError as e:
            for error in e.errors():
                field = error["loc"][0]
                kind  = error["type"]
                if kind == "missing":
                    raise MissingFields(f"campo obrigatório ausente: {field}")
                if field == "tipo":
                    raise InvalidTipo(f"tipo inválido: {data.tipo}")
                if field == "posicao":
                    raise InvalidPosicao(f"posicao inválida: {data.posicao}")
            raise MissingFields("dados inválidos")

    def create(self, data: FigurinhaCreate) -> FigurinhaOut:
        validated = self._validate_create(data)
        now = datetime.now()
        repo_data = CreateFigurinhaData(
            numero=validated.numero,
            nome=validated.nome,
            selecao=validated.selecao,
            tipo=validated.tipo.value,
            posicao=validated.posicao.value,
            created_at=now,
            updated_at=now,
        )
        return FigurinhaOut(**self.repo.create(repo_data))

    def list(self, posicao: str | None = None, tipo: str | None = None) -> list[FigurinhaOut]:
        if posicao and tipo:
            rows = self.repo.find_all_by_posicao_and_tipo({"posicao": posicao, "tipo": tipo})
        elif posicao:
            rows = self.repo.find_all_by_posicao({"posicao": posicao})
        elif tipo:
            rows = self.repo.find_all_by_tipo({"tipo": tipo})
        else:
            rows = self.repo.find_all()
        return [FigurinhaOut(**row) for row in rows]

    def get_by_id(self, id: int) -> FigurinhaOut:
        return FigurinhaOut(**self.repo.find_by_id(id))

    def update(self, id: int, data: FigurinhaUpdate) -> FigurinhaOut:
        validated = self._validate_update(data)
        repo_data = UpdateFigurinhaData(
            numero=validated.numero,
            nome=validated.nome,
            selecao=validated.selecao,
            tipo=validated.tipo.value,
            posicao=validated.posicao.value,
            updated_at=datetime.now(),
        )
        return FigurinhaOut(**self.repo.update(id, repo_data))

    def delete(self, id: int) -> None:
        self.repo.delete(id)
