import dataclasses
import sqlite3
from service.interfaces import FigurinhaRepository, CreateFigurinhaData, UpdateFigurinhaData
from repository.database.queries import Select, Insert, Update, Delete


class SQLiteFigurinhaRepository(FigurinhaRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _find_row(self, id: int) -> sqlite3.Row | None:
        return self.conn.execute(Select.BY_ID, {"id": id}).fetchone()

    def create(self, data: CreateFigurinhaData) -> dict:
        cursor = self.conn.execute(Insert.FIGURINHA, dataclasses.asdict(data))
        self.conn.commit()
        return dict(self._find_row(cursor.lastrowid))

    def find_all(self) -> list[dict]:
        return [dict(row) for row in self.conn.execute(Select.ALL).fetchall()]

    def find_all_by_posicao(self, data: dict) -> list[dict]:
        return [dict(row) for row in self.conn.execute(Select.BY_POSICAO, data).fetchall()]

    def find_all_by_tipo(self, data: dict) -> list[dict]:
        return [dict(row) for row in self.conn.execute(Select.BY_TIPO, data).fetchall()]

    def find_all_by_posicao_and_tipo(self, data: dict) -> list[dict]:
        return [dict(row) for row in self.conn.execute(Select.BY_POSICAO_AND_TIPO, data).fetchall()]

    def find_by_id(self, id: int) -> dict | None:
        row = self._find_row(id)
        return dict(row) if row else None

    def update(self, id: int, data: UpdateFigurinhaData) -> dict | None:
        if self._find_row(id) is None:
            return None
        self.conn.execute(Update.FIGURINHA, {"id": id, **dataclasses.asdict(data)})
        self.conn.commit()
        return dict(self._find_row(id))

    def delete(self, id: int) -> bool:
        if self._find_row(id) is None:
            return False
        self.conn.execute(Delete.FIGURINHA, {"id": id})
        self.conn.commit()
        return True
