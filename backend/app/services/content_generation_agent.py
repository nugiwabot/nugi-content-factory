import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.schemas.editorial_agent import (
    UserBriefInput,
    EditorialContentSpecification,
    VisualArtDirectionSpecification,
    ContentPackage,
    ContentType
)
from app.schemas.design_spec import DesignSpecification, CompositionType, CTAStrategy
from app.services.content_strategy_service import ContentStrategyService
from app.services.headline_service import HeadlineGenerationService
from app.services.caption_service import CaptionGenerationService
from app.services.creative_director_service import CreativeDirectorService
from app.rendering.editorial_renderer import EditorialRenderer
from app.services.visual_qa import VisualQAService
from app.providers.factory import ProviderFactory
from app.models.content import Content
from app.models.brief import ContentBrief
from app.models.asset import Asset
from app.core.logging import logger


class ContentGenerationAgent:
    """
    Master AI Agent orchestrating Content Strategy, Copywriting, Art Direction,
    Background Generation, Deterministic Pillow Rendering, QA, and Persistence.
    """
    def __init__(self):
        self.editorial_renderer = EditorialRenderer()

    def generate_full_package(
        self,
        brief: UserBriefInput,
        db: Optional[Session] = None,
        image_provider_type: Optional[str] = None
    ) -> ContentPackage:
        """
        Executes the full pipeline:
        Brief -> Strategy -> Headline -> Caption -> Art Direction -> Render -> QA -> DB Save.
        """
        logger.info(f"Starting AI Content & Art Direction generation for topic: {brief.topic}")

        # 1. Content Strategy & Framing
        strat = ContentStrategyService.classify_and_strategize(brief)

        # 2. Headline & Subheadline
        head_pkg = HeadlineGenerationService.generate_headline_package(
            topic=brief.topic,
            content_type=strat["content_type"],
            editorial_angle=strat["editorial_angle"],
            target_audience=strat["target_audience"]
        )

        # 3. Instagram Article Caption
        caption = CaptionGenerationService.generate_caption(
            topic=brief.topic,
            content_type=strat["content_type"],
            headline=head_pkg["headline"],
            core_insight=strat["core_insight"],
            target_audience=strat["target_audience"],
            cta_policy=strat["cta_policy"],
            cta_text=strat["cta_text"]
        )

        # 4. Assemble Editorial Content Specification
        key_points = [
            "Respon di atas 15 menit menurunkan closing 80%",
            "Template chat kaku tanpa personalisasi prospek",
            "Tidak membuat janji temu survey yang spesifik"
        ] if strat["content_type"] == ContentType.PROPERTY_LISTICLE else []

        metric_val = "+300%" if strat["content_type"] == ContentType.PROPERTY_CASE_STUDY else None
        metric_lbl = "Kecepatan Respon & Janji Survey" if strat["content_type"] == ContentType.PROPERTY_CASE_STUDY else None

        prop_loc = "Jatinangor, Sumedang" if strat["content_type"] == ContentType.PROPERTY_SHOWCASE else None
        prop_price = "Mulai Rp 1,85 Miliar" if strat["content_type"] == ContentType.PROPERTY_SHOWCASE else None
        prop_feat = ["16 Kamar Kost", "Yield 12%/thn", "SHM Siap"] if strat["content_type"] == ContentType.PROPERTY_SHOWCASE else []

        editorial_spec = EditorialContentSpecification(
            content_type=strat["content_type"],
            target_audience=strat["target_audience"],
            audience_problem=strat["audience_problem"],
            core_insight=strat["core_insight"],
            editorial_angle=strat["editorial_angle"],
            headline=head_pkg["headline"],
            subheadline=head_pkg["subheadline"],
            highlight_words=head_pkg["highlight_words"],
            caption=caption,
            key_points=key_points,
            suggested_archetype=strat["suggested_archetype"],
            cta_policy=strat["cta_policy"],
            cta_text=strat["cta_text"],
            metric_value=metric_val,
            metric_label=metric_lbl,
            property_location=prop_loc,
            property_price=prop_price,
            property_features=prop_feat
        )

        # 5. Visual Art Direction & Prompt Building
        art_direction = CreativeDirectorService.create_art_direction(editorial_spec)

        # 6. Build Design Specification Contract
        design_spec = CreativeDirectorService.build_design_specification(
            editorial_spec=editorial_spec,
            art_direction=art_direction,
            width=1080,
            height=1350
        )

        # 7. Generate Background Image (Flux with Mock Fallback)
        img_provider = ProviderFactory.get_image_provider(image_provider_type)
        bg_output = img_provider.generate_background(
            prompt=art_direction.image_prompt,
            width=design_spec.width,
            height=design_spec.height
        )

        # 8. Deterministic Typography & Layout Compositing
        rendered_bytes, meta = self.editorial_renderer.render(
            spec=design_spec,
            background_bytes=bg_output.image_bytes
        )

        # 9. Persist Asset to Storage
        storage = ProviderFactory.get_storage_provider()
        filename = f"content_{editorial_spec.content_type.value.lower()}_{uuid.uuid4().hex[:8]}_1080x1350.png"
        asset_path = storage.save(data=rendered_bytes, filename=filename, subfolder="generated")
        asset_url = f"/api/v1/assets/download?path={asset_path}"

        # 10. Automated Visual QA
        visual_qa = VisualQAService.evaluate_design(design_spec, meta)

        content_id = str(uuid.uuid4())

        # 11. Database Persistence (if DB session provided)
        if db and brief.project_id:
            try:
                db_content = Content(
                    id=content_id,
                    project_id=brief.project_id,
                    content_type=editorial_spec.content_type.value,
                    status="COMPLETED",
                    headline=editorial_spec.headline,
                    hook_text=editorial_spec.subheadline,
                    caption_body=editorial_spec.caption,
                    call_to_action=editorial_spec.cta_text or "",
                    hashtags="#Properti #NugiProperti",
                    design_template_id=design_spec.template_id,
                    primary_accent_color=design_spec.accent_color_hex,
                    visual_prompt=art_direction.image_prompt,
                    custom_metadata={
                        "archetype": art_direction.archetype.value,
                        "cta_policy": editorial_spec.cta_policy.value,
                        "highlight_words": editorial_spec.highlight_words,
                        "target_audience": editorial_spec.target_audience
                    }
                )
                db.add(db_content)

                db_asset = Asset(
                    id=str(uuid.uuid4()),
                    project_id=brief.project_id,
                    content_id=content_id,
                    asset_type="FINAL_IMAGE",
                    storage_path=asset_path,
                    mime_type="image/png",
                    width=design_spec.width,
                    height=design_spec.height,
                    file_size_bytes=len(rendered_bytes)
                )
                db.add(db_asset)
                db.commit()
            except Exception as dbe:
                logger.warning(f"DB persistence failed: {str(dbe)}. Proceeding in-memory.")
                db.rollback()

        return ContentPackage(
            content_id=content_id,
            project_id=brief.project_id,
            topic=brief.topic,
            content_type=editorial_spec.content_type,
            editorial_spec=editorial_spec,
            art_direction_spec=art_direction,
            design_spec=design_spec,
            rendered_asset_path=asset_path,
            rendered_asset_url=asset_url,
            visual_qa=visual_qa
        )

    def regenerate_headline(
        self,
        current_pkg: ContentPackage,
        custom_topic: Optional[str] = None
    ) -> ContentPackage:
        """Regenerates only the headline, subheadline, and highlight words without altering caption or visual."""
        topic = custom_topic or current_pkg.topic
        head_pkg = HeadlineGenerationService.generate_headline_package(
            topic=topic,
            content_type=current_pkg.content_type,
            editorial_angle=current_pkg.editorial_spec.editorial_angle,
            target_audience=current_pkg.editorial_spec.target_audience
        )

        current_pkg.editorial_spec.headline = head_pkg["headline"]
        current_pkg.editorial_spec.subheadline = head_pkg["subheadline"]
        current_pkg.editorial_spec.highlight_words = head_pkg["highlight_words"]

        current_pkg.design_spec.headline = head_pkg["headline"]
        current_pkg.design_spec.subheadline = head_pkg["subheadline"]
        current_pkg.design_spec.highlight_words = head_pkg["highlight_words"]

        # Re-render graphic
        rendered_bytes, meta = self.editorial_renderer.render(current_pkg.design_spec)
        storage = ProviderFactory.get_storage_provider()
        filename = f"content_rehead_{uuid.uuid4().hex[:8]}_1080x1350.png"
        asset_path = storage.save(data=rendered_bytes, filename=filename, subfolder="generated")
        current_pkg.rendered_asset_path = asset_path
        current_pkg.rendered_asset_url = f"/api/v1/assets/download?path={asset_path}"
        current_pkg.visual_qa = VisualQAService.evaluate_design(current_pkg.design_spec, meta)

        return current_pkg

    def regenerate_caption(
        self,
        current_pkg: ContentPackage
    ) -> ContentPackage:
        """Regenerates only the Instagram article caption."""
        caption = CaptionGenerationService.generate_caption(
            topic=current_pkg.topic,
            content_type=current_pkg.content_type,
            headline=current_pkg.editorial_spec.headline,
            core_insight=current_pkg.editorial_spec.core_insight,
            target_audience=current_pkg.editorial_spec.target_audience,
            cta_policy=current_pkg.editorial_spec.cta_policy,
            cta_text=current_pkg.editorial_spec.cta_text
        )
        current_pkg.editorial_spec.caption = caption
        return current_pkg

    def regenerate_visual_art(
        self,
        current_pkg: ContentPackage,
        archetype_override: Optional[CompositionType] = None
    ) -> ContentPackage:
        """Regenerates visual art direction, Flux prompt, and background composition."""
        if archetype_override:
            current_pkg.editorial_spec.suggested_archetype = archetype_override

        new_art = CreativeDirectorService.create_art_direction(current_pkg.editorial_spec)
        current_pkg.art_direction_spec = new_art

        new_design_spec = CreativeDirectorService.build_design_specification(
            editorial_spec=current_pkg.editorial_spec,
            art_direction=new_art,
            width=current_pkg.design_spec.width,
            height=current_pkg.design_spec.height
        )
        current_pkg.design_spec = new_design_spec

        # Generate fresh background and render
        img_provider = ProviderFactory.get_image_provider()
        bg_out = img_provider.generate_background(
            prompt=new_art.image_prompt,
            width=new_design_spec.width,
            height=new_design_spec.height
        )
        rendered_bytes, meta = self.editorial_renderer.render(new_design_spec, bg_out.image_bytes)

        storage = ProviderFactory.get_storage_provider()
        filename = f"content_reart_{uuid.uuid4().hex[:8]}_1080x1350.png"
        asset_path = storage.save(data=rendered_bytes, filename=filename, subfolder="generated")
        current_pkg.rendered_asset_path = asset_path
        current_pkg.rendered_asset_url = f"/api/v1/assets/download?path={asset_path}"
        current_pkg.visual_qa = VisualQAService.evaluate_design(new_design_spec, meta)

        return current_pkg
