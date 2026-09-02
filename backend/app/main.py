import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.errors import AppError, app_error_handler, generic_error_handler
from app.database import init_db
from app.api.v1.router import api_v1_router


def find_frontend_dist() -> Path | None:
    """Locates the built frontend static distribution directory."""
    exe_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path.cwd()
    meipass_dir = Path(getattr(sys, "_MEIPASS", "."))
    script_dir = Path(__file__).resolve().parent

    candidates = [
        meipass_dir / "frontend" / "dist",
        meipass_dir / "_internal" / "frontend" / "dist",
        exe_dir / "_internal" / "frontend" / "dist",
        exe_dir / "frontend" / "dist",
        script_dir.parent.parent.parent / "frontend" / "dist",
        script_dir.parent.parent / "frontend" / "dist",
        Path.cwd() / "frontend" / "dist",
        Path.cwd() / "dist",
    ]
    for c in candidates:
        if c.exists() and (c / "index.html").exists():
            return c.resolve()
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info(f"Starting {settings.APP_NAME} (v{settings.APP_VERSION}) on {settings.HOST}:{settings.PORT}")
    init_db()
    _seed_knowledge_base()
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME} gracefully.")


def _seed_knowledge_base() -> None:
    """Idempotently seeds skills, pillars, and brand context on startup."""
    try:
        from app.knowledge.source import KnowledgeSource
        KnowledgeSource.load_persisted()
        from app.database import SessionLocal
        from app.services.knowledge_service import KnowledgeService
        db = SessionLocal()
        try:
            KnowledgeService.seed_defaults(db)
        finally:
            db.close()
    except Exception:
        logger.exception("Knowledge base seeding failed (non-fatal).")


def create_app() -> FastAPI:
    """Application factory for FastAPI backend."""
    # Interactive docs are development conveniences; disabled in packaged/production mode.
    docs_enabled = not settings.is_production
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Internal AI Content Production System for Property Marketing",
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
        lifespan=lifespan
    )

    # 1. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Exception Handlers
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)

    # 3. Include API Routers
    app.include_router(api_v1_router)

    # 4. Frontend Static Files or Welcome JSON
    frontend_dist = find_frontend_dist()
    if frontend_dist:
        logger.info(f"Serving static frontend UI from: {frontend_dist}")
        
        # Mount assets folder if exists
        assets_dir = frontend_dist / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        @app.get("/")
        async def serve_spa_index(request: Request):
            accept = request.headers.get("accept", "")
            if settings.is_testing or ("application/json" in accept and "text/html" not in accept):
                return {
                    "app": settings.APP_NAME,
                    "version": settings.APP_VERSION,
                    "status": "operational",
                    "docs": "/docs",
                    "health": "/api/v1/health"
                }
            return FileResponse(frontend_dist / "index.html")

        # Catch-all for SPA client-side routes (excluding /api and /docs)
        @app.get("/{full_path:path}")
        async def serve_spa_fallback(full_path: str):
            if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi"):
                return JSONResponse(status_code=404, content={"error": "Not Found"})

            # Check if requested file exists directly (e.g. /nugi_properti_logo.png, /favicon.ico)
            # Resolve and enforce containment inside the frontend dist directory.
            dist_root = frontend_dist.resolve()
            static_file = (dist_root / full_path).resolve()
            try:
                static_file.relative_to(dist_root)
            except ValueError:
                return JSONResponse(status_code=404, content={"error": "Not Found"})

            if static_file.is_file():
                return FileResponse(static_file)

            return FileResponse(frontend_dist / "index.html")

    else:
        @app.get("/")
        def root():
            return {
                "app": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "status": "operational",
                "docs": "/docs",
                "health": "/api/v1/health"
            }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
