import json
from http.server import BaseHTTPRequestHandler
from service.interfaces import FigurinhaService
from domain.figurinha import FigurinhaNotFound, MissingFields, InvalidTipo, InvalidPosicao
from domain.schemas import FigurinhaCreate, FigurinhaUpdate


DOMAIN_ERRORS = {
    FigurinhaNotFound: 404,
    MissingFields:     400,
    InvalidTipo:       400,
    InvalidPosicao:    400,
}


class FigurinhaHandler:
    def __init__(self, service: FigurinhaService):
        self.service = service

    def _parse_body(self, handler: BaseHTTPRequestHandler) -> dict:
        content_type = handler.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise ValueError("Content-Type deve ser application/json")
        length = int(handler.headers.get("Content-Length", 0))
        if length == 0:
            raise ValueError("body ausente")
        return json.loads(handler.rfile.read(length))

    def _parse_id(self, path_segment: str) -> int:
        try:
            return int(path_segment)
        except (ValueError, TypeError):
            raise ValueError(f"id inválido: {path_segment}")

    def _send_json(self, handler: BaseHTTPRequestHandler, status: int, data) -> None:
        body = json.dumps(data, default=str).encode()
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(body)))
        handler.end_headers()
        handler.wfile.write(body)

    def _send_error(self, handler: BaseHTTPRequestHandler, status: int, message: str) -> None:
        self._send_json(handler, status, {"error": message})

    def _handle_domain_error(self, handler: BaseHTTPRequestHandler, exc: Exception) -> bool:
        for error_type, status in DOMAIN_ERRORS.items():
            if isinstance(exc, error_type):
                self._send_error(handler, status, str(exc) or error_type.__name__)
                return True
        return False

    # --- handlers das rotas ---

    def create(self, handler: BaseHTTPRequestHandler) -> None:
        try:
            body = self._parse_body(handler)
        except ValueError as e:
            self._send_error(handler, 400, str(e))
            return
        try:
            result = self.service.create(FigurinhaCreate(**body))
            self._send_json(handler, 201, result.model_dump())
        except Exception as e:
            if not self._handle_domain_error(handler, e):
                self._send_error(handler, 500, "erro interno")

    def list(self, handler: BaseHTTPRequestHandler, posicao: str | None, tipo: str | None) -> None:
        try:
            results = self.service.list(posicao, tipo)
            self._send_json(handler, 200, [r.model_dump() for r in results])
        except Exception as e:
            if not self._handle_domain_error(handler, e):
                self._send_error(handler, 500, "erro interno")

    def get_by_id(self, handler: BaseHTTPRequestHandler, id_str: str) -> None:
        try:
            id = self._parse_id(id_str)
        except ValueError as e:
            self._send_error(handler, 400, str(e))
            return
        try:
            result = self.service.get_by_id(id)
            self._send_json(handler, 200, result.model_dump())
        except Exception as e:
            if not self._handle_domain_error(handler, e):
                self._send_error(handler, 500, "erro interno")

    def update(self, handler: BaseHTTPRequestHandler, id_str: str) -> None:
        try:
            id = self._parse_id(id_str)
            body = self._parse_body(handler)
        except ValueError as e:
            self._send_error(handler, 400, str(e))
            return
        try:
            result = self.service.update(id, FigurinhaUpdate(**body))
            self._send_json(handler, 200, result.model_dump())
        except Exception as e:
            if not self._handle_domain_error(handler, e):
                self._send_error(handler, 500, "erro interno")

    def delete(self, handler: BaseHTTPRequestHandler, id_str: str) -> None:
        try:
            id = self._parse_id(id_str)
        except ValueError as e:
            self._send_error(handler, 400, str(e))
            return
        try:
            self.service.delete(id)
            handler.send_response(204)
            handler.end_headers()
        except Exception as e:
            if not self._handle_domain_error(handler, e):
                self._send_error(handler, 500, "erro interno")
