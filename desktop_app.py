import os
import sys
import time
import socket
import threading
import webbrowser
import multiprocessing
from pathlib import Path

# Provide safe stream wrappers if launched without console (pythonw / PyInstaller windowed)
class SafeStream:
    def write(self, text):
        pass
    def flush(self):
        pass
    def isatty(self):
        return False

if sys.stdout is None:
    sys.stdout = SafeStream()
if sys.stderr is None:
    sys.stderr = SafeStream()

# Add backend directory to sys.path
root_dir = Path(__file__).resolve().parent
if getattr(sys, "frozen", False):
    app_dir = Path(sys.executable).resolve().parent
    try:
        os.chdir(app_dir)
    except Exception:
        pass
    backend_dir = app_dir / "backend"
else:
    app_dir = root_dir
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
    """Finds an available local port on 127.0.0.1 by testing socket binding."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    return start_port


def wait_for_server(url: str, timeout_s: float = 20.0) -> bool:
    """Polls until the FastAPI server responds or timeout expires."""
    start_t = time.time()
    health_url = f"{url}/api/v1/health"
    while time.time() - start_t < timeout_s:
        try:
            with httpx.Client(timeout=1.0) as client:
                res = client.get(health_url)
                if res.status_code == 200:
                    logger.info(f"FastAPI server responded 200 OK at {health_url}")
                    return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def run_server(host: str, port: int):
    """Runs Uvicorn server in a dedicated thread with its own asyncio event loop."""
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        config = uvicorn.Config(
            app=fastapi_app,
            host=host,
            port=port,
            log_config=None,  # Prevent uvicorn from crashing on None sys.stderr in GUI mode
            access_log=False,
            loop="asyncio"
        )
        server = uvicorn.Server(config)
        loop.run_until_complete(server.serve())
    except Exception as e:
        logger.error(f"Fatal exception in FastAPI uvicorn thread: {e}", exc_info=True)


def main():
    setup_logging()
    logger.info("Initializing Nugi Content Factory Desktop Shell...")

    port = find_free_port(settings.PORT)
    host = "127.0.0.1"
    server_url = f"http://{host}:{port}"
    logger.info(f"Starting server on: {server_url}")

    # Start FastAPI server in background daemon thread
    server_thread = threading.Thread(
        target=run_server,
        args=(host, port),
        daemon=True,
        name="FastAPIServerThread"
    )
    server_thread.start()

    # Wait for server readiness before launching webview
    ready = wait_for_server(server_url, timeout_s=20.0)
    if not ready:
        logger.warning("Server readiness check timed out! Retrying health check once more...")
        time.sleep(2.0)

    # Try PyWebView Native Window with Edge WebView2
    opened_window = False
    try:
        import webview
        logger.info("Launching native desktop window via PyWebView (Edge WebView2)...")
        
        icon_path = root_dir / "assets" / "brand" / "app.ico"
        if not icon_path.exists():
            icon_path = None
        
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
    multiprocessing.freeze_support()
    main()
