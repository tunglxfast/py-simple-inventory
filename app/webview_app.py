import threading
import time

import uvicorn

from app.main import app


def run_server() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info")


def main() -> None:
    server = threading.Thread(target=run_server, daemon=True)
    server.start()
    time.sleep(1)
    try:
        import webview
    except ImportError as exc:
        raise RuntimeError("PyWebView chưa được cài đặt.") from exc
    webview.create_window("Quản lý kho", "http://127.0.0.1:8765", width=1280, height=800)
    webview.start()


if __name__ == "__main__":
    main()

