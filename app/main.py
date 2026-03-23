from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from app.config import settings
from app.services.todo_service import TodoService

service = TodoService()


class AppHandler(BaseHTTPRequestHandler):
    server_version = "BackendSkillsStarter/0.1"

    def _read_json(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def _send_json(self, status: int, payload: object | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        if payload is not None:
            self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "app": settings.app_name,
                    "environment": settings.environment,
                    "version": settings.version,
                },
            )
            return

        if path == "/skills":
            self._send_json(
                HTTPStatus.OK,
                {
                    "available": [
                        {
                            "name": "backend-api-baseline",
                            "purpose": "Scaffold CRUD handlers, services, validation, and tests.",
                        }
                    ]
                },
            )
            return

        if path == "/todos":
            self._send_json(HTTPStatus.OK, service.export_summary())
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/todos":
            payload = self._read_json()
            title = str(payload.get("title", "")).strip()
            if not title:
                self._send_json(HTTPStatus.BAD_REQUEST, {"detail": "title is required"})
                return
            item = service.create_item(title)
            self._send_json(HTTPStatus.CREATED, {"id": item.id, "title": item.title, "done": item.done})
            return

        if path.startswith("/todos/") and path.endswith("/complete"):
            item_id = path.removeprefix("/todos/").removesuffix("/complete").strip("/")
            try:
                item = service.mark_done(item_id)
            except KeyError:
                self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Todo not found"})
                return
            self._send_json(HTTPStatus.OK, {"id": item.id, "title": item.title, "done": item.done})
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Not found"})

    def do_DELETE(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path.startswith("/todos/"):
            item_id = path.removeprefix("/todos/").strip("/")
            service.delete_item(item_id)
            self._send_json(HTTPStatus.NO_CONTENT)
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Not found"})

    def log_message(self, format: str, *args: object) -> None:
        return


def run() -> None:
    httpd = ThreadingHTTPServer((settings.host, settings.port), AppHandler)
    print(f"Serving {settings.app_name} on http://{settings.host}:{settings.port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
