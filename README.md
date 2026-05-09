# Jeevn MVP - Repo scaffold

Jeevn is a minimal agricultural remote-sensing MVP that combines:

1. **A Python backend** for AOI ingestion, preprocessing, and anomaly detection
2. **A Streamlit UI** for submitting AOIs and viewing reports
3. **Clean-room interoperability contracts** that define how analysis agents should collaborate

## Local Setup

### Using Python virtualenv

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the API

```bash
uvicorn api.app:app --reload --port 8000
```

### Running the Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

### Using Docker Compose

```bash
docker compose -f infra/docker-compose.example.yml up --build -d
docker compose -f infra/docker-compose.example.yml down -v
```

## Repository Structure

- **`api/`** — FastAPI backend with AOI ingestion and report endpoints
- **`db/`** — SQLAlchemy models and database setup
- **`ingest/`** — Sentinel-2 metadata ingestion (stub and real paths)
- **`preproc/`** — NDVI, masking, aggregation, signal, detection, SAR, and texture helpers
- **`monitoring/`** — Prometheus metrics and MLflow integration
- **`ui/`** — Streamlit demo application
- **`scripts/`** — End-to-end smoke tests and dev helpers
- **`tests/`** — Pytest coverage for numerical and preprocessing logic
- **`docs/`** — Documentation
- **`infra/`** — Docker and infrastructure config

## Environment Variables

Optional configuration via environment variables:

- `DATABASE_URL` — SQLAlchemy database URL (defaults to SQLite)
- `SENTINEL_USER`, `SENTINEL_PASS` — Copernicus credentials for real Sentinel-2 metadata
- `DOWNLOAD_PRODUCTS` — Set to `1` to download Sentinel-2 products (optional, metadata-first by default)
- `MINIO_ENDPOINT`, `MINIO_BUCKET`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` — S3-compatible storage
- `API_URL` — Base URL for API (used by Streamlit UI)
- `MLFLOW_TRACKING_URI` — MLflow tracking server URL

## Architecture Notes

This repo combines two overlapping identities:

1. **Jeevn MVP** — A runnable agricultural remote-sensing system with a synchronous, in-memory-first design
2. **Clean-room interoperability scaffold** — Agent contracts and a handoff pipeline defined in root-level agent markdown and `plan.json`

The rough edges and known mismatches (e.g., UI/API payload shape differences) are preserved as part of the repo's current character.

## Testing

```bash
pytest -q
```

## License

See LICENSE file if present.
