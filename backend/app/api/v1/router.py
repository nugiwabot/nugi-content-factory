from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.projects import router as projects_router
from app.api.v1.brand_profiles import router as brands_router
from app.api.v1.briefs import router as briefs_router
from app.api.v1.content import router as content_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.assets import router as assets_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(brands_router)
api_v1_router.include_router(briefs_router)
api_v1_router.include_router(content_router)
api_v1_router.include_router(jobs_router)
api_v1_router.include_router(assets_router)
