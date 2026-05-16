import contextlib
import os
import socket
import threading
import time
from pathlib import Path

import uvicorn

from app.core.config import get_settings
from app.main import app

HOST = "127.0.0.1"
SERVER_START_TIMEOUT_SECONDS = 15
LOCK_FILENAME = "app.lock"


class SingleInstanceLock:
    def __init__(self, lock_path: Path) -> None:
        self.lock_path = lock_path
        self.file = None

    def acquire(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.lock_path.open("a+b")
        if self.file.tell() == 0:
            self.file.write(b"\0")
            self.file.flush()
        self.file.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            self.close()
            raise RuntimeError("Ứng dụng đang được mở ở một cửa sổ khác.") from exc

    def close(self) -> None:
        if not self.file:
            return
        with contextlib.suppress(OSError):
            if os.name == "nt":
                import msvcrt

                self.file.seek(0)
                msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
        self.file.close()
        self.file = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return int(sock.getsockname()[1])


def wait_for_server(host: str, port: int, timeout_seconds: int = SERVER_START_TIMEOUT_SECONDS) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("Không thể khởi động server nội bộ.")


def main() -> None:
    settings = get_settings()
    port = find_free_port()
    config = uvicorn.Config(app, host=HOST, port=port, log_level="info")
    uvicorn_server = uvicorn.Server(config)
    lock_path = settings.data_dir / LOCK_FILENAME

    try:
        import webview
    except ImportError as exc:
        raise RuntimeError("PyWebView chưa được cài đặt.") from exc

    with SingleInstanceLock(lock_path):
        server_thread = threading.Thread(target=uvicorn_server.run, daemon=True)
        server_thread.start()
        try:
            wait_for_server(HOST, port)
            webview.create_window("Quản lý kho", f"http://{HOST}:{port}", width=1280, height=800)
            webview.start()
        finally:
            uvicorn_server.should_exit = True
            server_thread.join(timeout=5)


if __name__ == "__main__":
    main()
