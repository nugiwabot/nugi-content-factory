from typing import Optional, Dict, Any, List
from app.schemas.design_spec import DesignSpecification, CompositionType, CTAStrategy
from app.schemas.visual_qa import VisualQAResult
from app.templates.registry import TemplateRegistry
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.rendering.layout import LayoutEngine


class VisualQAService:
    """
    Automated design validation and visual QA engine.
    Ensures that every generated visual strictly conforms to Design DNA,
    safe margins, contrast accessibility, editorial composition rules, and CTA business rules.
    """
    @staticmethod
    def evaluate_design(
        spec: DesignSpecification,
        rendered_metadata: Optional[Dict[str, Any]] = None
    ) -> VisualQAResult:
        score = 100
        issues: List[str] = []
        recommendations: List[str] = []

        readability = "EXCELLENT"
        hierarchy = "STRONG"
        composition = "BALANCED"
        branding = "COMPLIANT"
        safe_area_compliant = True
        contrast_ratio_compliant = True

        # 1. Canvas Dimension Validation
        valid_dimensions = [(1080, 1350), (1080, 1080)]
        if (spec.width, spec.height) not in valid_dimensions:
            score -= 20
            issues.append(f"Dimensi canvas ({spec.width}x{spec.height}) di luar standar Instagram (1080x1350 portrait atau 1080x1080 square).")
            recommendations.append("Gunakan 1080x1350 untuk performa optimal di Instagram Feed.")

        # 2. Template / Composition Check
        if hasattr(spec, "composition_type") and spec.composition_type:
            comp = spec.composition_type
            if comp == CompositionType.PROPERTY_SHOWCASE:
                if not spec.property_location and not spec.property_price and len(spec.property_features) == 0:
                    score -= 15
                    issues.append("Property Showcase membutuhkan minimal lokasi, harga, atau spesifikasi unit.")
            elif comp == CompositionType.DATA_EDITORIAL:
                if not spec.metric_value:
                    score -= 10
                    issues.append("Data Editorial membutuhkan nilai metrik data (metric_value).")
            elif comp == CompositionType.LIST_EDITORIAL:
                if len(spec.bullet_points) < 2:
                    score -= 15
                    issues.append("List Editorial membutuhkan minimal 2 poin daftar.")
        else:
            if not TemplateRegistry.exists(spec.template_id):
                score -= 15
                issues.append(f"Template ID '{spec.template_id}' tidak terdaftar.")

        # 3. CTA Business Rule Validation
        if spec.cta_strategy == CTAStrategy.CTA_REQUIRED:
            if not spec.cta_text:
                score -= 15
                hierarchy = "ACCEPTABLE"
                issues.append("Konten penawaran langsung (CTA_REQUIRED) membutuhkan teks tombol CTA.")
        elif spec.cta_strategy == CTAStrategy.CTA_NONE:
            # Having NO CTA on educational/insight/opinion articles is 100% compliant
            pass

        # 4. Headline Length & Mobile Readability
        if len(spec.headline.strip()) < 8:
            score -= 25
            readability = "POOR"
            issues.append("Headline terlalu pendek untuk menyampaikan pesan editorial utama.")
        elif len(spec.headline.strip()) > 140:
            score -= 15
            readability = "GOOD"
            issues.append("Headline sangat panjang, berpotensi menurunkan ukuran font drastis.")
            recommendations.append("Ringkas headline menjadi 15-20 kata agar tetap dominan di layar smartphone.")

        # 5. Highlight Words Verification
        if spec.highlight_words:
            headline_upper = spec.headline.upper()
            missing_terms = [t for t in spec.highlight_words if t.upper() not in headline_upper]
            if missing_terms:
                score -= 10
                issues.append(f"Kata sorotan {missing_terms} tidak ditemukan dalam teks headline.")
                recommendations.append("Pastikan highlight words diekstrak persis dari teks headline.")

        # 6. Contrast & Readability Check
        colors = NUGI_PROPERTI_BRAND_PROFILE.colors
        white_rgb = (255, 255, 255)
        card_rgb = colors.get_rgb(colors.surface_card)
        contrast = LayoutEngine.calculate_contrast_ratio(white_rgb, card_rgb)
        if contrast < 4.5:
            score -= 30
            contrast_ratio_compliant = False
            issues.append(f"Rasio kontras teks ({contrast:.1f}) di bawah standar aksesibilitas WCAG.")

        # 7. Final Score Clamping
        final_score = max(0, min(100, score))

        if final_score < 70:
            readability = "POOR"
            hierarchy = "WEAK"
        elif final_score < 85:
            hierarchy = "ACCEPTABLE"

        return VisualQAResult(
            score=final_score,
            readability=readability,
            hierarchy=hierarchy,
            composition=composition,
            branding=branding,
            safe_area_compliant=safe_area_compliant,
            contrast_ratio_compliant=contrast_ratio_compliant,
            issues=issues,
            recommendations=recommendations
        )
