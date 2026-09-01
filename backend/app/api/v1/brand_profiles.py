from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.brand_profile import BrandProfile
from app.schemas.brand_profile import BrandProfileCreate, BrandProfileResponse
from app.core.errors import NotFoundError, ValidationError

router = APIRouter(prefix="/brand-profiles", tags=["Brand Profiles"])


@router.get("", response_model=List[BrandProfileResponse])
def list_brand_profiles(db: Session = Depends(get_db)):
    """Lists all brand profiles."""
    return db.query(BrandProfile).order_by(BrandProfile.created_at.desc()).all()


@router.post("", response_model=BrandProfileResponse, status_code=status.HTTP_201_CREATED)
def create_brand_profile(payload: BrandProfileCreate, db: Session = Depends(get_db)):
    """Creates a new brand profile."""
    existing = db.query(BrandProfile).filter(BrandProfile.name == payload.name).first()
    if existing:
        raise ValidationError(f"Brand profile '{payload.name}' already exists.")

    brand = BrandProfile(
        name=payload.name,
        tagline=payload.tagline,
        primary_color=payload.primary_color,
        secondary_color=payload.secondary_color,
        accent_color=payload.accent_color,
        font_family=payload.font_family,
        logo_path=payload.logo_path,
        default_target_audience=payload.default_target_audience,
        default_cta_text=payload.default_cta_text,
        metadata_json=payload.metadata_json
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.get("/{brand_id}", response_model=BrandProfileResponse)
def get_brand_profile(brand_id: str, db: Session = Depends(get_db)):
    """Retrieves brand profile by ID."""
    brand = db.query(BrandProfile).filter(BrandProfile.id == brand_id).first()
    if not brand:
        raise NotFoundError("BrandProfile", brand_id)
    return brand
