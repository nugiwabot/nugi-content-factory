# 🏛️ Phase 03C: Visual Compositing Architecture

## 1. Overview & Evolution
Prior to Phase 3C, visual generation placed typography directly over a single flat background. Phase 3C transitions the architecture into a **13-Layer Editorial Compositing Pipeline**:

```
USER / AI BRIEF
       ↓
CONTENT STRATEGY (ContentStrategyService)
       ↓
CREATIVE DIRECTOR (CreativeDirectorService)
       ↓
VISUAL CONCEPT (VisualConceptSpecification)
       ↓
COMPOSITION PLAN (CompositionPlan)
       ↓
MULTI-ASSET GENERATION (FluxImageProvider / MockImageProvider)
       ↓
ASSET PROCESSING & ISOLATION (AssetCompositorService)
       ↓
COMPOSITING ENGINE (ProfessionalCompositingEngine)
       ↓
LIGHTING / SHADOW / DEPTH SIMULATION
       ↓
COLOR GRADING & CINEMATIC TONE MAPPING
       ↓
EDITORIAL GRAPHIC DESIGN ACCENTS
       ↓
DETERMINISTIC TYPOGRAPHY (LayoutEngine)
       ↓
VISUAL QA (VisualQAService)
       ↓
FINAL EXPORT (1080x1350 PNG)
```

---

## 2. The 13-Layer Compositing Stack

| Z-Index | Layer Name | Blend Mode | Purpose |
| :---: | :--- | :---: | :--- |
| **L0** | `Canvas Base` | Normal | Obsidian Navy background base (`#070B14`). |
| **L1** | `Background Asset` | Normal | Pure architectural photography (Flux 8k / Mock). |
| **L2** | `Atmosphere` | Screen / Normal | Twilight haze & ambient atmospheric gradient. |
| **L3** | `Architecture Scene` | Normal | Midground architectural geometry & facade depth. |
| **L4** | `Main Focal Subject` | Normal (Alpha) | Isolated persona / focal architectural asset. |
| **L5** | `Supporting Objects` | Normal (Alpha) | Metric pills, leads unread indicators. |
| **L6** | `Foreground Scrim` | Normal | Negative space gradient protecting text contrast. |
| **L7** | `Lighting Effects` | Screen / Add | Directional side light & subject rim light. |
| **L8** | `Shadows` | Multiply / Normal | Ground contact occlusion & directional drop shadow. |
| **L9** | `Depth Effects` | Normal | Multi-plane depth-of-field & corner vignette falloff. |
| **L10** | `Graphic Elements` | Normal | Eyebrow category badge, accent hairlines, dividers. |
| **L11** | `Typography` | Normal | Headline with word highlighting & subheadline. |
| **L12** | `Brand Identity` | Normal | Watermark signature & verified authority label. |

---

## 3. Core Engine Classes
- **`ProfessionalCompositingEngine`** (`backend/app/rendering/compositing_engine.py`): Pillow-based multi-layer compositor.
- **`AssetCompositorService`** (`backend/app/services/asset_compositor_service.py`): Multi-asset planning and subject alpha masking.
- **`CreativeDirectorService`** (`backend/app/services/creative_director_service.py`): Art direction, visual concepts, and 3-variant generation.
- **`ContentGenerationAgent`** (`backend/app/services/content_generation_agent.py`): Master orchestrator.
