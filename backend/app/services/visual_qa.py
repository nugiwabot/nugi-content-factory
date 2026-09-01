from typing import Optional, Dict, Any, List
from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    CTAStrategy,
    SAFEZONE_TOP,
    SAFEZONE_BOTTOM,
    SAFEZONE_HEIGHT,
    SAFEZONE_LEFT,
    SAFEZONE_RIGHT,
    SAFEZONE_CONTENT_LEFT,
    SAFEZONE_CONTENT_RIGHT
)
from app.schemas.visual_qa import VisualQAResult
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.rendering.layout import LayoutEngine


class VisualQAService:
    """
    Automated design validation and visual QA engine (Phase 3D-3 Safezone Enforcement).
    Evaluates:
    - Safezone & Crop Resilience: Safezone Pass, Critical Element Pass, Text Bounding Box Pass, Profile Grid Pass.
    - Multi-Category Pass: Technical Pass, Design Pass, Editorial Pass, Brand Pass.
    - Non-Regression Pass: Guarantees adherence to approved NugiProperti Editorial Design DNA.
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
        
        technical_pass = True
        design_pass = True
        editorial_pass = True
        brand_pass = True
        
        # Explicit Phase 3D-3 QA Passes
        safezone_pass = True
        safezone_critical_element_pass = True
        text_bounding_box_pass = True
        profile_grid_pass = True
        content_readability_pass = True
        non_regression_pass = True

        safe_area_compliant = True
        contrast_ratio_compliant = True

        safezone_bounds = {
            "top": SAFEZONE_TOP,
            "bottom": SAFEZONE_BOTTOM,
            "height": SAFEZONE_HEIGHT,
            "left_crop_3_4": 34,
            "right_crop_3_4": 34,
            "grid_3_4_width": 1012,
            "grid_3_4_height": 1350,
            "safezone_left": SAFEZONE_LEFT,
            "safezone_right": SAFEZONE_RIGHT,
            "safezone_content_left": SAFEZONE_CONTENT_LEFT,
            "safezone_content_right": SAFEZONE_CONTENT_RIGHT,
            "width": spec.width or 1080,
            "height": spec.height or 1350
        }

        # 1. Canvas Dimension Validation (1080x1350 with 4:5 Aspect Ratio)
        valid_dimensions = [(1080, 1350), (1080, 1080)]
        if (spec.width, spec.height) not in valid_dimensions:
            score -= 20
            technical_pass = False
            safezone_pass = False
            safe_area_compliant = False
            issues.append(f"Dimensi canvas ({spec.width}x{spec.height}) di luar standar Instagram 1080x1350.")
            recommendations.append("Gunakan resolusi 1080x1350 dengan safezone konten 1012x1080 (y=135..1215).")

        # 2. Critical Element Bounding Box Validation
        critical_bboxes = {}
        if rendered_metadata and "critical_element_bounding_boxes" in rendered_metadata:
            critical_bboxes = rendered_metadata["critical_element_bounding_boxes"]
            for elem_name, box in critical_bboxes.items():
                is_valid, elem_violations = LayoutEngine.validate_element_bounding_box(box, safezone_bounds)
                if not is_valid:
                    safezone_critical_element_pass = False
                    safezone_pass = False
                    text_bounding_box_pass = False
                    score -= 10
                    issues.append(f"Elemen kritis '{elem_name}' melanggar safezone: {', '.join(elem_violations)}")
                    recommendations.append(f"Sesuaikan posisi vertikal/horizontal '{elem_name}' agar berada di dalam x=76..1004, y=135..1215.")

        # 3. Instagram 3:4 Profile Grid Resilience Check
        for elem_name, box in critical_bboxes.items():
            l = box.get("left", 0)
            r = box.get("right", 0)
            if l < SAFEZONE_LEFT or r > SAFEZONE_RIGHT:
                profile_grid_pass = False
                safezone_pass = False
                score -= 15
                issues.append(f"Elemen kritis '{elem_name}' akan terpotong pada tampilan grid profil Instagram 3:4.")

        # 4. Template / Archetype Check
        if hasattr(spec, "composition_type") and spec.composition_type:
            comp = spec.composition_type
            if comp == CompositionType.PROPERTY_SHOWCASE:
                if not spec.property_location and not spec.property_price and len(spec.property_features) == 0:
                    score -= 10
                    editorial_pass = False
                    issues.append("Property Showcase membutuhkan minimal lokasi, harga, atau spesifikasi unit.")
            elif comp == CompositionType.DATA_EDITORIAL:
                if not spec.metric_value:
                    score -= 10
                    editorial_pass = False
                    issues.append("Data Editorial membutuhkan nilai metrik data (metric_value).")
            elif comp == CompositionType.LIST_EDITORIAL:
                if len(spec.bullet_points) < 2:
                    score -= 10
                    editorial_pass = False
                    issues.append("List Editorial membutuhkan minimal 2 poin daftar.")

        # 5. CTA Business Rule Validation
        if spec.cta_strategy == CTAStrategy.CTA_REQUIRED:
            if not spec.cta_text:
                score -= 15
                editorial_pass = False
                hierarchy = "ACCEPTABLE"
                issues.append("Konten penawaran langsung (CTA_REQUIRED) membutuhkan teks tombol CTA.")
        elif spec.cta_strategy == CTAStrategy.CTA_NONE:
            # Having NO CTA on editorial/insight/opinion is 100% compliant
            pass

        # 6. Headline Length & Mobile Impact
        if len(spec.headline.strip()) < 8:
            score -= 25
            editorial_pass = False
            readability = "POOR"
            content_readability_pass = False
            issues.append("Headline terlalu pendek untuk menyampaikan pesan editorial utama.")
        elif len(spec.headline.strip()) > 150:
            score -= 15
            editorial_pass = False
            readability = "GOOD"
            issues.append("Headline sangat panjang, berpotensi menurunkan ukuran font drastis.")
            recommendations.append("Ringkas headline menjadi 10-18 kata agar tetap bold dan dominan di safezone.")

        # 7. Highlight Words Verification
        if spec.highlight_words:
            headline_upper = spec.headline.upper()
            missing_terms = [t for t in spec.highlight_words if t.upper() not in headline_upper]
            if missing_terms:
                score -= 5
                issues.append(f"Kata sorotan {missing_terms} tidak ditemukan dalam teks headline.")
                recommendations.append("Pastikan highlight words diekstrak persis dari teks headline.")

        # 8. Contrast & Readability Check (WCAG AAA)
        colors = NUGI_PROPERTI_BRAND_PROFILE.colors
        white_rgb = (255, 255, 255)
        card_rgb = colors.get_rgb(colors.surface_card)
        contrast = LayoutEngine.calculate_contrast_ratio(white_rgb, card_rgb)
        if contrast < 4.5:
            score -= 25
            design_pass = False
            contrast_ratio_compliant = False
            content_readability_pass = False
            issues.append(f"Rasio kontras teks ({contrast:.1f}) di bawah standar aksesibilitas WCAG.")

        # 9. Brand Compliance Check
        if not spec.brand_name:
            score -= 10
            brand_pass = False
            branding = "NON_COMPLIANT"
            issues.append("Nama brand tidak boleh kosong.")

        # 10. Non-Regression Assessment
        if not technical_pass or not design_pass or not brand_pass or not editorial_pass:
            non_regression_pass = False

        # 11. Overall Quality Classification
        final_score = max(0, min(100, score))
        if final_score >= 90 and technical_pass and design_pass and editorial_pass and brand_pass and safezone_pass:
            overall_quality = "EXCELLENT"
        elif final_score >= 75:
            overall_quality = "GOOD"
        elif final_score >= 60:
            overall_quality = "ACCEPTABLE"
        else:
            overall_quality = "NEEDS_IMPROVEMENT"

        return VisualQAResult(
            score=final_score,
            readability=readability,
            hierarchy=hierarchy,
            composition=composition,
            branding=branding,
            technical_pass=technical_pass,
            design_pass=design_pass,
            editorial_pass=editorial_pass,
            brand_pass=brand_pass,
            safezone_pass=safezone_pass,
            safezone_critical_element_pass=safezone_critical_element_pass,
            text_bounding_box_pass=text_bounding_box_pass,
            profile_grid_pass=profile_grid_pass,
            content_readability_pass=content_readability_pass,
            non_regression_pass=non_regression_pass,
            overall_quality=overall_quality,
            safe_area_compliant=safe_area_compliant,
            contrast_ratio_compliant=contrast_ratio_compliant,
            safezone_bounds=safezone_bounds,
            critical_element_bounding_boxes=critical_bboxes,
            issues=issues,
            recommendations=recommendations
        )
