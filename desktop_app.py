import os
import sys
import time
import socket
import threading
import webbrowser
from pathlib import Path

# Add backend directory to sys.path
root_dir = Path(__file__).resolve().parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Enable Production Desktop Mode
os.environ["APP_ENV"] = "production"

import uvicorn
import httpx
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.main import app as fastapi_app


def find_free_port(start_port: int = 8000, max_attempts: int = 50) -> int:
    """Finds an available local port on 127.0.0.1."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


def wait_for_server(url: str, timeout_s: float = 12.0) -> bool:
    """Polls until the FastAPI server responds or timeout expires."""
    start_t = time.time()
    health_url = f"{url}/api/v1/health"
    while time.time() - start_t < timeout_s:
        try:
            with httpx.Client(timeout=1.0) as client:
                res = client.get(health_url)
                if res.status_code == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def run_server(host: str, port: int):
    """Runs Uvicorn server in a dedicated thread."""
    config = uvicorn.Config(
        app=fastapi_app,
        host=host,
        port=port,
        log_level="warning",
        access_log=False
    )
    server = uvicorn.Server(config)
    server.run()


def main():
    setup_logging()
    logger.info("Initializing Nugi Content Factory Desktop Shell...")

    port = find_free_port(settings.PORT)
    host = "127.0.0.1"
    server_url = f"http://{host}:{port}"
    logger.info(f"Targeting local server URL: {server_url}")

    # Start FastAPI server in background daemon thread
    server_thread = threading.Thread(
        target=run_server,
        args=(host, port),
        daemon=True,
        name="FastAPIServerThread"
    )
    server_thread.start()

    # Wait for server readiness
    if not wait_for_server(server_url):
        logger.warning("Server startup check timed out; attempting to open window anyway.")

    # Try PyWebView Native Window with Edge WebView2
    opened_window = False
    try:
        import webview
        logger.info("Launching native desktop window via PyWebView (Edge WebView2)...")
        
        icon_path = root_dir / "assets" / "brand" / "app.ico"
        
        window = webview.create_window(
            title="Nugi Content Factory — Property Edition",
            url=server_url,
            width=1280,
            height=860,
            min_size=(1024, 700),
            background_color="#040711"
        )
        
        # Start PyWebView event loop (blocks until window is closed)
        webview.start(gui="edgechromium", debug=False)
        opened_window = True
        logger.info("Desktop window closed by user.")

    except ImportError:
        logger.info("pywebview not installed; launching default browser window.")
    except Exception as e:
        logger.warning(f"Native window launch encountered: {e}; falling back to browser.")

    # Fallback to default browser if webview was not used
    if not opened_window:
        webbrowser.open(server_url)
        print(f"\n=======================================================")
        print(f" Nugi Content Factory running on: {server_url}")
        print(f" Press Ctrl+C in this terminal to exit.")
        print(f"=======================================================\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Exiting application...")

    logger.info("Nugi Content Factory shutdown clean.")
    sys.exit(0)


if __name__ == "__main__":
    main()
