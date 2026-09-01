# ⚙️ Configuration Reference: Nugi Content Factory

Sistem konfigurasi menggunakan Pydantic Settings yang secara otomatis membaca environment variables dan file `.env`.

## Daftar Variabel Konfigurasi

| Variabel | Tipe | Default | Deskripsi |
| :--- | :--- | :--- | :--- |
| `APP_ENV` | String | `development` | Environment runtime: `development`, `testing`, `production`. |
| `DEBUG` | Boolean | `true` | Mengaktifkan output log debug dan endpoint docs. |
| `HOST` | String | `127.0.0.1` | Alamat IP host server FastAPI. |
| `PORT` | Integer | `8000` | Port listen API server. |
| `DATABASE_URL` | String | `sqlite:///./nugi_content_factory.db` | Connection string database SQLAlchemy (SQLite / PostgreSQL). |
| `STORAGE_PROVIDER` | String | `local` | Driver penyimpanan asset (`local`). |
| `STORAGE_BASE_DIR` | String | `./storage/assets` | Direktori lokal tempat penyimpanan file render PNG. |
| `LLM_PROVIDER` | String | `mock` | Driver LLM yang aktif (`mock`, `openai`, `anthropic`). |
| `IMAGE_PROVIDER` | String | `mock` | Driver image generator (`mock`, `flux`). |
| `OPENAI_API_KEY` | String | `None` | API Key OpenAI (opsional untuk live mode masa depan). |
| `ANTHROPIC_API_KEY`| String | `None` | API Key Anthropic (opsional). |
| `FLUX_API_KEY` | String | `None` | API Key BFL / Flux (opsional). |

## Keamanan API Key & Secrets
1. File `.env` masuk dalam `.gitignore` dan tidak akan pernah di-commit ke Git repository.
2. Semua secret di-load secara aman di backend dan **tidak pernah dikirimkan ke frontend client**.
