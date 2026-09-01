from fastapi import APIRouter
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE, BrandProfileSpec

router = APIRouter(prefix="/brand", tags=["Brand Intelligence"])


@router.get("/nugi-properti", response_model=BrandProfileSpec)
def get_nugi_properti_profile():
    """Returns official NugiProperti Brand Profile, Design DNA & Semantic Design Tokens."""
    return NUGI_PROPERTI_BRAND_PROFILE
