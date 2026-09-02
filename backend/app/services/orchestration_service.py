import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.brief import ContentBrief
from app.models.brand_profile import BrandProfile
from app.models.content import Content
from app.models.asset import Asset
from app.models.qa_result import QAResult
from app.models.generation_log import GenerationLog
from app.models.job import GenerationJob

from app.providers.factory import ProviderFactory
from app.providers.retry import call_with_retry
from app.rendering.engine import DeterministicRenderingEngine
from app.services.job_service import JobService
from app.services.qa_service import QAService
from app.core.errors import NotFoundError, AppError
from app.core.logging import logger


class OrchestrationService:
    """
    Coordinates the multi-stage AI reasoning, background generation,
    deterministic graphic rendering, QA evaluation, and persistence pipeline.
    """
    def __init__(self):
        self.rendering_engine = DeterministicRenderingEngine()

    def generate_single_content(
        self,
        db: Session,
        project_id: str,
        topic: str,
        target_audience: str,
        content_pillar: str = "educational",
        tone_of_voice: str = "professional_authoritative",
        brief_id: Optional[str] = None,
        brand_profile_id: Optional[str] = None,
        llm_provider_type: Optional[str] = None,
        image_provider_type: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Verify Project
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project", project_id)

        # 2. Resolve Brand Profile
        brand_profile = None
        if brand_profile_id:
            brand_profile = db.query(BrandProfile).filter(BrandProfile.id == brand_profile_id).first()
        elif project.brand_profile_id:
            brand_profile = db.query(BrandProfile).filter(BrandProfile.id == project.brand_profile_id).first()

        brand_name = brand_profile.name if brand_profile else "NugiProperti Studio"
        primary_color = brand_profile.primary_color if brand_profile else "#0f172a"
        accent_color = brand_profile.secondary_color if brand_profile else "#38bdf8"

        # 3. Create Generation Job Record
        job = JobService.create_job(
            db=db,
            project_id=project_id,
            brief_id=brief_id,
            job_type="single_content_generation",
            payload={"topic": topic, "audience": target_audience, "pillar": content_pillar}
        )

        try:
            # 4. Stage 1: LLM Copywriting & Reasoning
            JobService.update_progress(db, job, progress=25, status="RUNNING")
            llm_provider = ProviderFactory.get_llm_provider(llm_provider_type)
            
            llm_output = call_with_retry(
                llm_provider.generate_content,
                topic=topic,
                target_audience=target_audience,
                content_pillar=content_pillar,
                tone_of_voice=tone_of_voice,
                brand_context={"brand_name": brand_name}
            )

            # Log LLM Stage
            llm_log = GenerationLog(
                job_id=job.id,
                provider_type="LLM",
                provider_name=llm_provider.provider_name,
                model_name="mock-property-v1",
                prompt_text=f"Topic: {topic} | Audience: {target_audience}",
                response_payload=llm_output.model_dump(),
                latency_ms=llm_output.latency_ms,
                status="SUCCESS"
            )
            db.add(llm_log)

            # 5. Stage 2: Background Image Generation
            JobService.update_progress(db, job, progress=50, status="RUNNING")
            image_provider = ProviderFactory.get_image_provider(image_provider_type)
            
            img_output = call_with_retry(
                image_provider.generate_background,
                prompt=llm_output.visual_concept_prompt,
                width=1080,
                height=1080
            )

            # Log Image Generation Stage
            img_log = GenerationLog(
                job_id=job.id,
                provider_type="ImageGenerator",
                provider_name=image_provider.provider_name,
                model_name="mock-canvas-v1",
                prompt_text=llm_output.visual_concept_prompt,
                response_payload={"width": img_output.width, "height": img_output.height},
                latency_ms=img_output.latency_ms,
                status="SUCCESS"
            )
            db.add(img_log)

            # Save Raw Background Asset via StorageProvider
            storage = ProviderFactory.get_storage_provider()
            bg_filename = f"bg_{uuid.uuid4().hex[:10]}.png"
            bg_path = storage.save(img_output.image_bytes, bg_filename, subfolder="backgrounds")

            # 6. Stage 3: Deterministic Graphic Rendering
            JobService.update_progress(db, job, progress=75, status="RUNNING")
            rendered_bytes, render_meta = self.rendering_engine.render(
                background_bytes=img_output.image_bytes,
                headline=llm_output.headline,
                category_badge=content_pillar.replace("_", " ").upper(),
                hook_text=llm_output.hook_text,
                brand_name=brand_name,
                primary_color_hex=primary_color,
                accent_color_hex=accent_color,
                width=1080,
                height=1080
            )

            final_filename = f"rendered_{uuid.uuid4().hex[:10]}.png"
            final_path = storage.save(rendered_bytes, final_filename, subfolder="rendered")

            # 7. Stage 4: Deterministic QA Evaluation
            qa_eval = QAService.evaluate(
                headline=llm_output.headline,
                body_caption=llm_output.body_caption,
                category_badge=content_pillar,
                brand_colors={"primary": primary_color, "accent": accent_color}
            )

            # 8. Stage 5: Database Entities Persistence
            content_item = Content(
                project_id=project_id,
                brief_id=brief_id,
                brand_profile_id=brand_profile.id if brand_profile else None,
                headline=llm_output.headline,
                hook_text=llm_output.hook_text,
                body_caption=llm_output.body_caption,
                hashtags=llm_output.hashtags,
                call_to_action=llm_output.call_to_action,
                visual_concept_prompt=llm_output.visual_concept_prompt,
                status="QA_PASSED" if qa_eval["status"] == "PASSED" else "DRAFT",
                metadata_json={"render_metadata": render_meta}
            )
            db.add(content_item)
            db.flush() # Populate content_item.id

            # Save Final Asset Record
            final_asset = Asset(
                project_id=project_id,
                content_id=content_item.id,
                asset_type="rendered_final",
                file_path=final_path,
                file_url=f"/api/v1/assets/download?path={final_path}",
                mime_type="image/png",
                width=1080,
                height=1080,
                file_size_bytes=len(rendered_bytes),
                metadata_json=render_meta
            )
            db.add(final_asset)

            # Save QA Result Record
            qa_record = QAResult(
                content_id=content_item.id,
                status=qa_eval["status"],
                contrast_score=qa_eval["contrast_score"],
                text_overflow_detected=qa_eval["text_overflow_detected"],
                headline_length_chars=qa_eval["headline_length_chars"],
                body_length_chars=qa_eval["body_length_chars"],
                issues_json=qa_eval["issues"],
                recommendations_json=qa_eval["recommendations"]
            )
            db.add(qa_record)

            # Update logs with content_id
            llm_log.content_id = content_item.id
            img_log.content_id = content_item.id

            # Complete Job
            result_payload = {
                "content_id": content_item.id,
                "asset_id": final_asset.id,
                "image_path": final_path,
                "headline": content_item.headline,
                "qa_status": qa_eval["status"]
            }
            JobService.complete_job(db, job, result=result_payload)
            db.commit()

            return {
                "success": True,
                "job_id": job.id,
                "content_id": content_item.id,
                "headline": content_item.headline,
                "hook_text": content_item.hook_text,
                "body_caption": content_item.body_caption,
                "hashtags": content_item.hashtags,
                "call_to_action": content_item.call_to_action,
                "asset_path": final_path,
                "asset_url": final_asset.file_url,
                "qa_result": qa_eval,
                "render_metadata": render_meta
            }

        except Exception as e:
            db.rollback()
            JobService.fail_job(db, job, error_message=str(e))
            logger.exception(f"Orchestration pipeline failed for Project {project_id}: {str(e)}")
            raise AppError(f"Content generation orchestration failed: {str(e)}")
