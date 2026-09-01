# 🗄️ Data Model Reference: Nugi Content Factory

## 1. Entity Relationship Overview

```
BrandProfile (1) ───< (N) Project (1) ───< (N) ContentBrief
                                 │                      │
                                 │                      │
                                 └──< (N) Content (N) >─┘
                                             │
                                             ├──< (N) Asset
                                             ├──< (N) QAResult
                                             └──< (N) GenerationLog
```

## 2. Core Entities

### `projects`
* `id` (UUID PK): Identifier unik project.
* `name` (String): Nama project (misal: "GREN Propertykost Jatinangor").
* `slug` (String Unique): URL/path safe slug.
* `description` (Text): Catatan konteks project.
* `brand_profile_id` (UUID FK): Relasi ke brand guidelines default.

### `brand_profiles`
* `id` (UUID PK): Identifier unik.
* `name` (String Unique): Nama brand/agensi.
* `primary_color`, `secondary_color`, `accent_color` (Hex): Palet warna rendering.
* `font_family` (String): Font render.
* `logo_path` (String): Path ke file logo brand.
* `default_target_audience` (String): Persona default.
* `default_cta_text` (String): CTA penutup default.

### `content_briefs`
* `id` (UUID PK): Identifier unik.
* `project_id` (UUID FK): Relasi project.
* `title` (String): Judul brief.
* `topic` (Text): Ide pokok materi pemasaran.
* `target_audience` (String): Target pembaca.
* `content_pillar` (String): `educational`, `authority`, `direct_offer`, `case_study`.
* `tone_of_voice` (String): Gaya bahasa.

### `contents`
* `id` (UUID PK): Identifier unik.
* `project_id` (UUID FK), `brief_id` (UUID FK), `brand_profile_id` (UUID FK).
* `headline` (String): Teks judul banner visual.
* `hook_text` (String): Subtitle/hook pembuka.
* `body_caption` (Text): Copywriting lengkap postingan.
* `hashtags` (String): Tagar.
* `call_to_action` (String): Instruksi tindakan audiens.
* `visual_concept_prompt` (Text): Prompt model gambar.
* `status` (String): `DRAFT`, `QA_PASSED`, `APPROVED`, `ARCHIVED`.

### `assets`
* `id` (UUID PK): Identifier unik.
* `content_id` (UUID FK), `project_id` (UUID FK).
* `asset_type` (String): `background_raw`, `rendered_final`, `logo`.
* `file_path` (String): Lokasi penyimpanan lokal.
* `width`, `height`, `file_size_bytes` (Integer).

### `generation_jobs`
* `id` (UUID PK): Identifier unik job.
* `status` (String): `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`.
* `progress_percentage` (Integer 0-100).
* `job_payload`, `job_result` (JSON).

### `qa_results`
* `id` (UUID PK): Identifier unik.
* `content_id` (UUID FK).
* `status` (String): `PASSED`, `WARNING`, `FAILED`.
* `contrast_score` (Float): Skor kontras WCAG.
* `issues_json`, `recommendations_json` (JSON List).

### `generation_logs`
* `id` (UUID PK): Identifier unik.
* `job_id` (UUID FK), `content_id` (UUID FK).
* `provider_type`, `provider_name`, `model_name` (String).
* `prompt_text` (Text), `response_payload` (JSON).
* `latency_ms` (Integer), `status` (String).
