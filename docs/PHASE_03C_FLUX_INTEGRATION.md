# ⚡ Phase 03C: Flux Integration & Graceful Fallback System

## 1. Flux Image Provider Specification

* **Provider Class:** `FluxImageProvider` (`backend/app/providers/flux_image.py`).
* **Environment Variables:**
  - `FLUX_API_KEY`: API authentication key.
  - `FLUX_MODEL`: Target model (e.g. `flux.1-schnell` or `flux.1-dev`).
  - `FLUX_BASE_URL`: REST API endpoint.

## 2. Zero-Crash Fallback Workflow

```
Flux API Call
     ↓
[Is API Key Valid & Network Available?]
   ├── YES ➔ Return Flux 8k Photographic Asset
   └── NO / ERROR ➔ Log Warning & Seamlessly Delegate to MockImageProvider
```

* **Security Guardrail:** API keys are never exposed in log outputs or client error responses.
* **Asset Purity Rule:** Prompts strictly prohibit text, typography, watermarks, or logos to keep raw visual assets clean for deterministic compositing.
