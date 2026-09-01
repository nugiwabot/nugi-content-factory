# 💻 Technology Stack: Nugi Content Factory

| Komponen | Teknologi Terpilih | Alasan Pemilihan & Arsitektur |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.10+ / FastAPI | Asynchronous performance tinggi, automatic OpenAPI/Swagger documentation, dan ekosistem AI/Image processing terbaik. |
| **ORM & Database** | SQLAlchemy 2.0 / SQLite / PostgreSQL | Mendukung SQLite untuk zero-setup local dev dan desktop packaging, serta siap digunakan dengan PostgreSQL untuk deployment server. |
| **Data Validation** | Pydantic v2 & Pydantic Settings | Strict type validation, serialization cepat, dan pengelolaan environment variables yang aman. |
| **Image Processing** | Python Pillow (PIL) | Deterministic rendering engine untuk tipografi pixel-perfect, compositing layer, dan kalkulasi kontras warna. |
| **Frontend Framework** | React 18 + Vite 5 | Fast build time, hot module replacement instan, dan struktur komponen modular. |
| **Styling** | Vanilla CSS Design Tokens | Bebas dari bloat library CSS eksternal, kontrol penuh atas palet dark mode, dan performa tinggi. |
| **Icons** | Lucide React | Ikon modern, tajam, dan ringan. |
| **HTTP Client** | Axios (Frontend) / HTTPX (Backend) | Request/Response interceptor yang handal dan timeout configuration. |
| **Testing** | Pytest + Pytest-Asyncio + TestClient | Automated test suite komprehensif untuk unit, provider, rendering, dan API endpoints. |
