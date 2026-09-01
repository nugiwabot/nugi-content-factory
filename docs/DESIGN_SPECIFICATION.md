# 📋 Design Specification Schema: Nugi Content Factory

`DesignSpecification` adalah kontrak data resmi yang menghubungkan proses reasoning AI dengan mesin *deterministic rendering*.

---

## 1. Schema Properties

```python
class DesignSpecification(BaseModel):
    template_id: str = "01_PROPERTY_PROBLEM"
    width: int = 1080
    height: int = 1350 # 1350 portrait feed (4:5) atau 1080 square (1:1)
    
    headline: str # Teks headline utama
    highlight_words: List[str] = [] # Kata/frasa sorotan yang diberi warna aksen
    subheadline: Optional[str] = None # Penjelasan pendukung
    badge_text: Optional[str] = None # Label kategori atas
    
    bullet_points: List[str] = [] # Khusus template listicle (03_NUMBER_LIST)
    metric_value: Optional[str] = None # Khusus template case study (04_CASE_STUDY)
    metric_label: Optional[str] = None # Label metrik
    cta_text: Optional[str] = None # Teks tombol Call to Action
    
    brand_name: str = "NugiProperti"
    show_logo: bool = True
    background_type: str = "gradient" # gradient | image | solid
    background_image_path: Optional[str] = None
    accent_color_hex: Optional[str] = None
```

---

## 2. Contoh Payload Input Real

```json
{
  "template_id": "01_PROPERTY_PROBLEM",
  "width": 1080,
  "height": 1350,
  "headline": "LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?",
  "highlight_words": ["LAMBAT FOLLOW-UP"],
  "subheadline": "Setiap menit keterlambatan bisa membuat prospek berpindah ke kompetitor.",
  "badge_text": "DILEMA SALES PROPERTI",
  "cta_text": "Pelajari Solusinya →",
  "brand_name": "NugiProperti"
}
```
Mesin render otomatis memecah baris (*line wrapping*), menghitung font fitting, memisahkan segmen kata sorotan, dan menghasilkan output PNG 1080x1350 beresolusi tinggi.
