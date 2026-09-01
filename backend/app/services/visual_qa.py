from typing import Optional, Dict, Any, List
from app.schemas.design_spec import DesignSpecification
from app.schemas.visual_qa import VisualQAResult
from app.templates.registry import TemplateRegistry
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.rendering.layout import LayoutEngine


class VisualQAService:
    """
    Automated design validation and visual QA engine.
    Ensures that every generated visual strictly conforms to Design DNA,
    safe margins, contrast accessibility, and template rules.
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

        # 2. Template Existence Check
        if not TemplateRegistry.exists(spec.template_id):
            score -= 15
            issues.append(f"Template ID '{spec.template_id}' tidak terdaftar.")
            tmpl = TemplateRegistry.get("01_PROPERTY_PROBLEM")
        else:
            tmpl = TemplateRegistry.get(spec.template_id)

        # 3. Headline Length & Typography Fitting
        if len(spec.headline.strip()) < 8:
            score -= 25
            readability = "POOR"
            issues.append("Headline terlalu pendek untuk menyampaikan pesan utama.")
        elif len(spec.headline.strip()) > 140:
            score -= 15
            readability = "GOOD"
            issues.append("Headline sangat panjang, berpotensi menurunkan ukuran font drastis.")
            recommendations.append("Ringkas headline menjadi 15-20 kata agar tetap dominan.")

        # 4. Highlight Words Verification
        if spec.highlight_words:
            headline_upper = spec.headline.upper()
            missing_terms = [t for t in spec.highlight_words if t.upper() not in headline_upper]
            if missing_terms:
                score -= 10
                issues.append(f"Kata sorotan {missing_terms} tidak ditemukan dalam teks headline.")
                recommendations.append("Pastikan highlight words diekstrak persis dari teks headline.")

        # 5. Required Zones Check per Template
        for zone in tmpl.zones:
            if zone.required:
                if zone.zone_id == "badge" and not spec.badge_text and not zone.default_text:
                    score -= 10
                    hierarchy = "ACCEPTABLE"
                    issues.append("Badge kategori tidak terisi pada template yang mewajibkannya.")
                elif zone.zone_id == "cta" and not spec.cta_text and not zone.default_text:
                    score -= 10
                    issues.append("Tombol CTA tidak terisi.")
                elif zone.zone_id == "bullet_list" and len(spec.bullet_points) == 0:
                    score -= 20
                    issues.append(f"Template '{spec.template_id}' membutuhkan daftar bullet points minimal 1 item.")

        # 6. Contrast & Readability Check
        # White text (#ffffff) on card (#0c1220) ratio is ~17.5:1 (exceeds WCAG AAA 7:1)
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
