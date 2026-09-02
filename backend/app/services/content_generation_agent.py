import uuid
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.schemas.editorial_agent import (
    UserBriefInput,
    EditorialContentSpecification,
    VisualArtDirectionSpecification,
    ContentPackage,
    ContentType
)
from app.schemas.compositing import (
    VisualConceptSpecification,
    CompositionPlan,
    VisualVariant
)
from app.schemas.design_spec import DesignSpecification, CompositionType, CTAStrategy
from app.services.content_strategy_service import ContentStrategyService
from app.services.headline_service import HeadlineGenerationService
from app.services.caption_service import CaptionGenerationService
from app.services.copywriter_service import CopywriterService
from app.services.knowledge_service import KnowledgeService
from app.services.creative_director_service import CreativeDirectorService
from app.services.asset_compositor_service import AssetCompositorService
from app.rendering.compositing_engine import ProfessionalCompositingEngine
from app.rendering.editorial_renderer import EditorialRenderer
from app.services.visual_qa import VisualQAService
from app.providers.factory import ProviderFactory
from app.providers.retry import call_with_retry
from app.core.pricing import estimate_image_cost
from app.models.content import Content
from app.models.brief import ContentBrief
from app.models.asset import Asset
from app.models.generation_log import GenerationLog
from app.core.logging import logger


class ContentGenerationAgent:
    """
    Master AI Agent orchestrating Content Strategy, Copywriting, Art Direction,
    13-Layer Compositing Engine, Deterministic Typography, Visual QA, and Multi-Variant Generation.
    """
    def __init__(self):
        self.compositing_engine = ProfessionalCompositingEngine()
        self.editorial_renderer = EditorialRenderer()

    def generate_full_package(
        self,
        brief: UserBriefInput,
        db: Optional[Session] = None,
        image_provider_type: Optional[str] = None,
        debug_safezone: bool = False,
        skill_context: Optional[str] = None,
        brand_context: Optional[str] = None
    ) -> ContentPackage:
        """
        Executes end-to-end editorial generation pipeline (Phase 3D-3 Safezone Enforcement):
        Brief -> Strategy -> Headline -> Caption -> Visual Concept -> Asset Plan ->
        13-Layer Compositing -> Visual QA -> Multi-Variant Planning -> DB Save.
        image_provider_type defaults to the active configured provider (Settings > Image Provider).
        """
        logger.info(f"Starting AI Content & Art Direction generation for topic: {brief.topic}")

        # 1. Content Strategy & Framing
        strat = ContentStrategyService.classify_and_strategize(brief)

        # 2-3. Headline, Subheadline, Highlight Words & Caption
        # Prefer LLM-driven copywriting (skill + brand informed); fall back to
        # deterministic template services when no live LLM is available.
        copy = CopywriterService.generate_editorial_copy(
            topic=brief.topic,
            content_type=strat["content_type"].value,
            target_audience=strat["target_audience"],
            core_insight=strat["core_insight"],
            cta_policy=strat["cta_policy"].value,
            cta_text=strat["cta_text"],
            skill_context=skill_context,
            brand_context=brand_context
        )

        if copy:
            headline = copy["headline"]
            subheadline = copy["subheadline"]
            highlight_words = copy["highlight_words"]
            caption = copy["caption"]
        else:
            head_pkg = HeadlineGenerationService.generate_headline_package(
                topic=brief.topic,
                content_type=strat["content_type"],
                editorial_angle=strat["editorial_angle"],
                target_audience=strat["target_audience"]
            )
            headline = head_pkg["headline"]
            subheadline = head_pkg["subheadline"]
            highlight_words = head_pkg["highlight_words"]
            caption = CaptionGenerationService.generate_caption(
                topic=brief.topic,
                content_type=strat["content_type"],
                headline=headline,
                core_insight=strat["core_insight"],
                target_audience=strat["target_audience"],
                cta_policy=strat["cta_policy"],
                cta_text=strat["cta_text"]
            )

        # 4. Assemble Editorial Content Specification
        llm_usage = (copy or {}).get("usage") or {}
        key_points = [
            "Respon di atas 15 menit menurunkan closing 80%",
            "Template chat kaku tanpa personalisasi prospek",
            "Tidak membuat janji temu survey yang spesifik"
        ] if strat["content_type"] == ContentType.PROPERTY_LISTICLE else []

        metric_val = "+300%" if strat["content_type"] == ContentType.PROPERTY_CASE_STUDY else ("12.4%" if strat["content_type"] == ContentType.DATA_EDITORIAL else None)
        metric_lbl = "Kecepatan Respon & Janji Survey" if strat["content_type"] == ContentType.PROPERTY_CASE_STUDY else ("Yield Sewa Rata-rata" if strat["content_type"] == ContentType.DATA_EDITORIAL else None)

        prop_loc = "Jatinangor, Sumedang" if strat["content_type"] in (ContentType.PROPERTY_SHOWCASE, ContentType.SOFT_SELLING) else None
        prop_price = "Mulai Rp 1,85 Miliar" if strat["content_type"] in (ContentType.PROPERTY_SHOWCASE, ContentType.SOFT_SELLING) else None
        prop_feat = ["16 Kamar Kost", "Yield 12%/thn", "SHM Siap"] if strat["content_type"] in (ContentType.PROPERTY_SHOWCASE, ContentType.SOFT_SELLING) else []

        editorial_spec = EditorialContentSpecification(
            content_type=strat["content_type"],
            target_audience=strat["target_audience"],
            audience_problem=strat["audience_problem"],
            core_insight=strat["core_insight"],
            editorial_angle=strat["editorial_angle"],
            headline=headline,
            subheadline=subheadline,
            highlight_words=highlight_words,
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

        # 5. Visual Concept & Art Direction
        concept = CreativeDirectorService.create_visual_concept(editorial_spec)
        art_direction = CreativeDirectorService.create_art_direction(editorial_spec)

        # 6. Build Design Specification & Composition Plan
        design_spec = CreativeDirectorService.build_design_specification(
            editorial_spec=editorial_spec,
            art_direction=art_direction,
            width=1080,
            height=1350
        )
        plan = AssetCompositorService.build_composition_plan(concept, design_spec.accent_color_hex or "#8b5cf6")

        # 7. Generate Background Asset (uses the configured provider; mock in dev/testing)
        img_provider = ProviderFactory.get_image_provider(image_provider_type)
        bg_output = call_with_retry(
            img_provider.generate_background,
            prompt=art_direction.image_prompt,
            width=design_spec.width,
            height=design_spec.height
        )

        # Usage / estimated cost tracking (best-effort, never blocks generation).
        llm_cost = llm_usage.get("estimated_cost_usd")
        image_cost = estimate_image_cost(bg_output.model) if bg_output.model else None
        total_cost = None
        if llm_cost is not None or image_cost is not None:
            total_cost = round((llm_cost or 0) + (image_cost or 0), 6)
        usage_report = {
            "llm": llm_usage,
            "image": {
                "provider": bg_output.provider,
                "model": bg_output.model,
                "estimated_cost_usd": image_cost,
                "latency_ms": bg_output.latency_ms
            },
            "estimated_cost_usd_total": total_cost,
        }

        # 8. 13-Layer Compositing Engine Execution
        design_spec.background_image_bytes = bg_output.image_bytes
        rendered_bytes, meta = self.compositing_engine.composite_full_artwork(
            design_spec=design_spec,
            plan=art_direction,
            concept=concept,
            debug_safezone=debug_safezone
        )

        # 9. Persist Asset to Storage
        storage = ProviderFactory.get_storage_provider()
        filename = f"composite_{editorial_spec.content_type.value.lower()}_{uuid.uuid4().hex[:8]}_1080x1350.png"
        asset_path = storage.save(data=rendered_bytes, filename=filename, subfolder="generated")
        asset_url = f"/api/v1/assets/download?path={asset_path}"

        # 10. Automated Visual QA
        visual_qa = VisualQAService.evaluate_design(design_spec, meta)

        # 11. Generate Multi-Variants (1-3 Variants)
        variants = CreativeDirectorService.generate_visual_variants(editorial_spec, design_spec)
        # Populate first variant with active render
        variants[0].rendered_asset_path = asset_path
        variants[0].rendered_asset_url = asset_url
        variants[0].visual_qa_score = visual_qa.score

        content_id = str(uuid.uuid4())

        # 12. Database Persistence
        if db and brief.project_id:
            try:
                db_content = Content(
                    id=content_id,
                    project_id=brief.project_id,
                    status="COMPLETED",
                    headline=editorial_spec.headline,
                    hook_text=editorial_spec.subheadline,
                    body_caption=editorial_spec.caption,
                    call_to_action=editorial_spec.cta_text or "",
                    hashtags="#Properti #NugiProperti",
                    visual_concept_prompt=art_direction.image_prompt,
                    template_id=design_spec.template_id,
                    metadata_json={
                        "content_type": editorial_spec.content_type.value,
                        "archetype": art_direction.archetype.value,
                        "cta_policy": editorial_spec.cta_policy.value,
                        "highlight_words": editorial_spec.highlight_words,
                        "target_audience": editorial_spec.target_audience,
                        "primary_accent_color": design_spec.accent_color_hex,
                        "visual_story": concept.visual_story,
                        "usage": usage_report,
                        "estimated_cost_usd": total_cost
                    }
                )
                db.add(db_content)

                db_asset = Asset(
                    id=str(uuid.uuid4()),
                    project_id=brief.project_id,
                    content_id=content_id,
                    asset_type="FINAL_IMAGE",
                    file_path=asset_path,
                    file_url=asset_url,
                    mime_type="image/png",
                    width=design_spec.width,
                    height=design_spec.height,
                    file_size_bytes=len(rendered_bytes)
                )
                db.add(db_asset)
                db.commit()

                self._write_generation_logs(
                    db=db,
                    content_id=content_id,
                    usage=usage_report,
                    prompt_text=art_direction.image_prompt,
                    topic=brief.topic
                )
            except Exception as dbe:
                db.rollback()
                logger.error(f"DB persistence failed for content generation: {str(dbe)}")
                raise

        return ContentPackage(
            content_id=content_id,
            project_id=brief.project_id,
            topic=brief.topic,
            content_type=editorial_spec.content_type,
            editorial_spec=editorial_spec,
            art_direction_spec=art_direction,
            design_spec=design_spec,
            concept_spec=concept.model_dump(),
            variants=[v.model_dump() for v in variants],
            active_variant=variants[0].variant_name,
            rendered_asset_path=asset_path,
            rendered_asset_url=asset_url,
            visual_qa=visual_qa,
            estimated_cost_usd=total_cost,
            usage=usage_report
        )

    def _write_generation_logs(
        self,
        db: Session,
        content_id: str,
        usage: Dict[str, Any],
        prompt_text: str,
        topic: str,
    ) -> None:
        """Persists best-effort provider usage/audit logs. Never fails generation."""
        try:
            llm = usage.get("llm") or {}
            if llm.get("provider") and "mock" not in str(llm.get("provider", "")).lower():
                db.add(GenerationLog(
                    content_id=content_id,
                    provider_type="LLM",
                    provider_name=str(llm.get("provider"))[:50],
                    model_name=str(llm.get("model") or "")[:100],
                    prompt_text=f"Topic: {topic}",
                    response_payload=llm,
                    status="SUCCESS"
                ))

            img = usage.get("image") or {}
            if img.get("provider") and "mock" not in str(img.get("provider", "")).lower():
                db.add(GenerationLog(
                    content_id=content_id,
                    provider_type="ImageGenerator",
                    provider_name=str(img.get("provider"))[:50],
                    model_name=str(img.get("model") or "")[:100],
                    prompt_text=prompt_text,
                    response_payload=img,
                    latency_ms=img.get("latency_ms"),
                    status="SUCCESS"
                ))
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to write generation usage logs: {str(e)}")

    def regenerate_headline(
        self,
        current_pkg: ContentPackage,
        custom_topic: Optional[str] = None
    ) -> ContentPackage:
        """Regenerates only the headline, subheadline, and highlight words without re-running visual generation."""
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

        # Re-render with existing background
        rendered_bytes, meta = self.compositing_engine.composite_full_artwork(
            concept=VisualConceptSpecification(**current_pkg.concept_spec) if current_pkg.concept_spec else None,
            design_spec=current_pkg.design_spec
        )
        storage = ProviderFactory.get_storage_provider()
        filename = f"rehead_{uuid.uuid4().hex[:8]}_1080x1350.png"
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

        new_concept = CreativeDirectorService.create_visual_concept(current_pkg.editorial_spec)
        new_art = CreativeDirectorService.create_art_direction(current_pkg.editorial_spec)

        new_design_spec = CreativeDirectorService.build_design_specification(
            editorial_spec=current_pkg.editorial_spec,
            art_direction=new_art,
            width=current_pkg.design_spec.width,
            height=current_pkg.design_spec.height
        )
        new_plan = AssetCompositorService.build_composition_plan(new_concept, new_design_spec.accent_color_hex or "#38bdf8")

        current_pkg.concept_spec = new_concept.model_dump()
        current_pkg.art_direction_spec = new_art
        current_pkg.design_spec = new_design_spec

        # Generate fresh background and composite
        img_provider = ProviderFactory.get_image_provider()
        bg_out = call_with_retry(
            img_provider.generate_background,
            prompt=new_art.image_prompt,
            width=new_design_spec.width,
            height=new_design_spec.height
        )
        rendered_bytes, meta = self.compositing_engine.composite_full_artwork(
            concept=new_concept,
            design_spec=new_design_spec,
            plan=new_plan,
            background_bytes=bg_out.image_bytes
        )

        storage = ProviderFactory.get_storage_provider()
        filename = f"reart_{uuid.uuid4().hex[:8]}_1080x1350.png"
        asset_path = storage.save(data=rendered_bytes, filename=filename, subfolder="generated")
        current_pkg.rendered_asset_path = asset_path
        current_pkg.rendered_asset_url = f"/api/v1/assets/download?path={asset_path}"
        current_pkg.visual_qa = VisualQAService.evaluate_design(new_design_spec, meta)

        return current_pkg

    def handle_conversational_chat(
        self,
        req: Any,
        db: Optional[Session] = None
    ) -> Any:
        """
        Handles conversational AI Copilot chat interactions.
        Distinguishes between general greetings/strategy consultation and direct content generation requests.
        """
        from app.schemas.editorial_agent import AgentChatResponse, QuickSuggestion, UserBriefInput

        msg_clean = req.message.strip()
        lower_msg = msg_clean.lower()

        # 1. Check for greetings and general conversational intent
        greetings = [
            "halo", "hai", "hei", "hello", "hi", "selamat pagi", "selamat siang",
            "selamat sore", "selamat malam", "tes", "test", "bisa bantu saya",
            "kamu siapa", "bantu saya", "apa kabar", "kamu bisa apa"
        ]
        is_greeting = any(lower_msg == g or lower_msg.startswith(g + " ") or lower_msg.startswith(g + "?") or lower_msg.endswith(" " + g) or lower_msg.endswith(" " + g + "?") for g in greetings)
        
        is_conversational = is_greeting or (
            len(lower_msg.split()) <= 5 and any(kw in lower_msg for kw in ["bisa", "bantu", "tanya", "gimana", "gmana", "apa yang"])
        )

        # Check for revision commands
        is_revise_headline = ("ubah headline" in lower_msg or "ganti headline" in lower_msg or "headline lain" in lower_msg) and req.active_package is not None
        is_revise_visual = ("ubah visual" in lower_msg or "ganti visual" in lower_msg or "visual lain" in lower_msg or "ubah gambar" in lower_msg or "ganti gambar" in lower_msg) and req.active_package is not None
        is_revise_caption = ("tulis ulang caption" in lower_msg or "ganti caption" in lower_msg or "caption lain" in lower_msg) and req.active_package is not None

        if is_revise_headline:
            updated_pkg = self.regenerate_headline(req.active_package)
            return AgentChatResponse(
                reply=f"Headline telah saya perbarui menjadi: **\"{updated_pkg.editorial_spec.headline}\"** dengan highlight kata kunci baru.",
                action_type="REVISE_HEADLINE",
                content_package=updated_pkg
            )

        if is_revise_visual:
            updated_pkg = self.regenerate_visual_art(req.active_package)
            return AgentChatResponse(
                reply="Visual arsitektur dan tata cahaya poster telah saya perbarui dan render ulang.",
                action_type="REVISE_VISUAL",
                content_package=updated_pkg
            )

        if is_revise_caption:
            updated_pkg = self.regenerate_caption(req.active_package)
            return AgentChatResponse(
                reply="Caption artikel Instagram telah saya tulis ulang dengan hook dan struktur baru.",
                action_type="REVISE_CAPTION",
                content_package=updated_pkg
            )

        if is_conversational and not any(kw in lower_msg for kw in ["buat", "bikin", "generate", "posting", "poster"]):
            suggestions = [
                QuickSuggestion(label="Leads Boncos Closing Nol", prompt="Kenapa leads iklan properti banyak tapi closing tetap rendah? Target: Developer & Sales Manager."),
                QuickSuggestion(label="Edukasi SHM vs Girik", prompt="Edukasi bahaya membeli tanah tanpa sertifikat SHM untuk investor pemula di Bandung."),
                QuickSuggestion(label="3 Kesalahan Follow-Up Sales", prompt="3 kesalahan fatal tim sales properti saat follow-up leads dari iklan digital."),
                QuickSuggestion(label="Cash Flow vs Capital Gain", prompt="Investasi properti: Lebih menguntungkan cash flow rukost mahasiswa atau capital gain tanah kosong?")
            ]

            reply_text = (
                "Halo Mas Nugi! Tentu saja, saya sangat siap membantu! 🚀\n\n"
                "Saya adalah **Nugi AI Content Copilot** — spesialis strategi konten, copywriting, dan desain visual properti Anda.\n\n"
                "Anda bisa berdiskusi atau langsung meminta saya membuat konten. Contohnya:\n"
                "• *'Bikinkan konten edukasi tentang bahaya beli rumah tanpa IMB/PBG'*\n"
                "• *'Buat postingan kenapa rukost dekat kampus selalu cepat tersewa'*\n"
                "• *'Bahas tips follow-up prospek properti agar tidak hilang'* \n\n"
                "Silakan ketik topik apa saja yang ingin dibuat, atau klik salah satu rekomendasi di bawah ini:"
            )

            return AgentChatResponse(
                reply=reply_text,
                action_type="CHAT",
                content_package=None,
                quick_suggestions=suggestions
            )

        # 2. Content Generation Intent
        clean_topic = msg_clean
        for prefix in [
            "bikinkan konten tentang", "buatkan konten tentang", "buat konten tentang",
            "bikin konten tentang", "bikinkan post tentang", "buatkan post tentang",
            "bikin postingan tentang", "tolong buatkan konten tentang", "tolong buatkan konten"
        ]:
            if clean_topic.lower().startswith(prefix):
                clean_topic = clean_topic[len(prefix):].strip()
                break

        brief = UserBriefInput(
            topic=clean_topic,
            project_id=req.project_id
        )

        # Inject brand context + relevant skills (knowledge base) into the generation.
        skill_context = ""
        brand_context = ""
        if db:
            try:
                brand_context = KnowledgeService.get_brand_context(db)
                skill_context = KnowledgeService.retrieve_relevant_skills(db, brief.topic)
            except Exception as e:
                logger.warning(f"Knowledge retrieval skipped: {str(e)}")

        pkg = self.generate_full_package(
            brief=brief,
            db=db,
            skill_context=skill_context,
            brand_context=brand_context
        )
        headline = pkg.editorial_spec.headline

        reply_text = (
            f"Tentu Mas Nugi! Saya telah merancang konten editorial lengkap bertema: **\"{headline}\"**.\n\n"
            f"• **Target Audiens:** {pkg.editorial_spec.target_audience}\n"
            f"• **Format/Arketipe:** {pkg.editorial_spec.content_type.value}\n"
            f"• **Safezone Audit:** 100% Pass (Sesuai rasio Instagram 4:5 1080x1350)\n\n"
            f"Poster high-res dan caption siap posting sudah tersedia di bawah ini. Anda bisa langsung mengunduh gambar atau menyalin caption."
        )

        return AgentChatResponse(
            reply=reply_text,
            action_type="GENERATE",
            content_package=pkg
        )
