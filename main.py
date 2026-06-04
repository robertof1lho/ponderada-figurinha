from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from repository.database.connection import init_db, get_db
from repository.sqlite_figurinha import SQLiteFigurinhaRepository
from service.figurinha_service import FigurinhaServiceImpl
from handler.figurinha_handler import FigurinhaHandler


def make_request_handler(handler: FigurinhaHandler):
    class RequestHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            print(f"[{self.command}] {self.path} → {args[1] if len(args) > 1 else ''}")

        def _route(self):
            parsed = urlparse(self.path)
            parts  = [p for p in parsed.path.split("/") if p]
            query  = parse_qs(parsed.query)

            # /figurinha
            if parts == ["figurinha"]:
                return "list", query
            # /figurinha/{id}
            if len(parts) == 2 and parts[0] == "figurinha":
                return "item", parts[1]
            return None, None

        def do_GET(self):
            route, extra = self._route()
            if route == "list":
                posicao = extra.get("posicao", [None])[0]
                tipo    = extra.get("tipo",    [None])[0]
                handler.list(self, posicao, tipo)
            elif route == "item":
                handler.get_by_id(self, extra)
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            route, _ = self._route()
            if route == "list":
                handler.create(self)
            else:
                self.send_response(404)
                self.end_headers()

        def do_PUT(self):
            route, extra = self._route()
            if route == "item":
                handler.update(self, extra)
            else:
                self.send_response(404)
                self.end_headers()

        def do_DELETE(self):
            route, extra = self._route()
            if route == "item":
                handler.delete(self, extra)
            else:
                self.send_response(404)
                self.end_headers()

    return RequestHandler


def main():
    init_db()
    db_gen = get_db()
    conn   = next(db_gen)

    repo    = SQLiteFigurinhaRepository(conn)
    service = FigurinhaServiceImpl(repo)
    h       = FigurinhaHandler(service)

    server = HTTPServer(("0.0.0.0", 8000), make_request_handler(h))
    print("Servidor rodando em http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        next(db_gen, None)


if __name__ == "__main__":
    main()
