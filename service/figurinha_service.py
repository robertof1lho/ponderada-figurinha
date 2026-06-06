from datetime import datetime
from pydantic import ValidationError
from service.interfaces import FigurinhaRepository, FigurinhaService, CreateFigurinhaData, UpdateFigurinhaData
from domain.figurinha import FigurinhaCreate, FigurinhaUpdate, FigurinhaOut
from service.interfaces import FigurinhaNotFound, MissingFields, InvalidTipo, InvalidPosicao


class FigurinhaServiceImpl(FigurinhaService):
    def __init__(self, repo: FigurinhaRepository):
        self.repo = repo

    def _validate_create(self, data: dict) -> FigurinhaCreate:
        try:
            return FigurinhaCreate(**data)
        except ValidationError as e:
            for error in e.errors():
                field = error["loc"][0]
                kind  = error["type"]
                if kind == "missing":
                    raise MissingFields(f"campo obrigatório ausente: {field}")
                if field == "tipo":
                    raise InvalidTipo(f"tipo inválido: {data.get('tipo')}")
                if field == "posicao":
                    raise InvalidPosicao(f"posicao inválida: {data.get('posicao')}")
            raise MissingFields("dados inválidos")

    def _validate_update(self, data: dict) -> FigurinhaUpdate:
        try:
            return FigurinhaUpdate(**data)
        except ValidationError as e:
            for error in e.errors():
                field = error["loc"][0]
                kind  = error["type"]
                if kind == "missing":
                    raise MissingFields(f"campo obrigatório ausente: {field}")
                if field == "tipo":
                    raise InvalidTipo(f"tipo inválido: {data.get('tipo')}")
                if field == "posicao":
                    raise InvalidPosicao(f"posicao inválida: {data.get('posicao')}")
            raise MissingFields("dados inválidos")

    def create(self, data: dict) -> FigurinhaOut:
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
        row = self.repo.find_by_id(id)
        if row is None:
            raise FigurinhaNotFound()
        return FigurinhaOut(**row)

    def update(self, id: int, data: dict) -> FigurinhaOut:
        validated = self._validate_update(data)
        repo_data = UpdateFigurinhaData(
            numero=validated.numero,
            nome=validated.nome,
            selecao=validated.selecao,
            tipo=validated.tipo.value,
            posicao=validated.posicao.value,
            updated_at=datetime.now(),
        )
        row = self.repo.update(id, repo_data)
        if row is None:
            raise FigurinhaNotFound()
        return FigurinhaOut(**row)

    def delete(self, id: int) -> None:
        if not self.repo.delete(id):
            raise FigurinhaNotFound()
