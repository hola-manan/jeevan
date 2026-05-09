"""
Jeevn - MVP API
FastAPI backend for agricultural remote-sensing workflows
"""
import os
import json
import uuid
import threading
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

# Optional dependencies - graceful fallback if not available
try:
    from db import db, models
    DB_AVAILABLE = True
except (ImportError, Exception):
    DB_AVAILABLE = False

try:
    from monitoring import metrics
    MONITORING_AVAILABLE = True
except (ImportError, Exception):
    MONITORING_AVAILABLE = False

try:
    from ingest import sentinels_ingest
    INGEST_AVAILABLE = True
except (ImportError, Exception):
    INGEST_AVAILABLE = False

try:
    from preproc import run_preproc
    PREPROC_AVAILABLE = True
except (ImportError, Exception):
    PREPROC_AVAILABLE = False

# FastAPI app initialization
app = FastAPI(title="Jeevn - MVP API", version="1.0.0")

# In-memory AOI store - primary runtime store (thread-safe)
AOI_STORE: Dict[str, Dict[str, Any]] = {}
AOI_STORE_LOCK = threading.Lock()

# Pydantic models for request/response
class AOIRequest(BaseModel):
    name: str
    geojson: dict
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Sample AOI",
            "geojson": {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [0.0, 0.0],
                            [1.0, 0.0],
                            [1.0, 1.0],
                            [0.0, 1.0],
                            [0.0, 0.0]
                        ]]
                    }
                }]
            },
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
    })

class HealthResponse(BaseModel):
    status: str

class AOIResponse(BaseModel):
    aoi_id: str
    metadata_path: Optional[str] = None
    ndvi_csv: Optional[str] = None
    ndvi_timeseries: Optional[list] = None
    ndvi_raster: Optional[str] = None
    parcel_confidence: Optional[Dict[str, Any]] = None
    anomalies: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    aoi_id: str
    status: str
    metadata_path: Optional[str] = None
    report: Optional[Dict[str, Any]] = None

# Endpoints

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/aoi", response_model=AOIResponse)
def create_aoi(request: AOIRequest):
    """
    Create a new AOI and trigger ingestion/preprocessing workflow.
    
    Flow:
    1. Store AOI in in-memory dictionary
    2. Optionally create DB records if DB integration is available
    3. Call ingest helper to produce metadata JSON
    4. Attempt NDVI time-series aggregation
    5. Attempt cloud-masked NDVI raster generation
    6. Compute parcel-confidence summary if raster exists
    7. Store report payload in-memory
    """
    
    try:
        # Create AOI ID as UUID object
        aoi_id = uuid.uuid4()
        aoi_id_str = str(aoi_id)
        
        # Store in AOI_STORE (primary runtime store) - thread-safe
        aoi_record = {
            "id": aoi_id_str,
            "name": request.name,
            "geojson": request.geojson,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "created_at": datetime.utcnow().isoformat(),
            "status": "created"
        }
        with AOI_STORE_LOCK:
            AOI_STORE[aoi_id_str] = aoi_record
        
        # Optionally create DB records if DB available
        if DB_AVAILABLE:
            try:
                db.init_db()
                session = db.SessionLocal()
                db_aoi = models.AOI(
                    id=aoi_id,
                    name=request.name,
                    geojson_data=request.geojson,
                    start_date=request.start_date,
                    end_date=request.end_date
                )
                session.add(db_aoi)
                session.commit()
                session.close()
            except Exception as db_err:
                print(f"[INFO] DB integration skipped: {db_err}")
        
        # Initialize report structure
        metadata_path = None
        ndvi_csv = None
        ndvi_timeseries = None
        ndvi_raster = None
        parcel_confidence = None
        anomalies = None
        
        # Call ingest helper if available
        if INGEST_AVAILABLE:
            try:
                ingest_result = sentinels_ingest.ingest(
                    aoi_geojson=request.geojson,
                    start_date=request.start_date,
                    end_date=request.end_date,
                    aoi_id=aoi_id
                )
                metadata_path = ingest_result.get("metadata_path")
                
                # Optionally create ingest job record if DB available
                if DB_AVAILABLE:
                    try:
                        session = db.SessionLocal()
                        ingest_job = models.IngestJob(
                            aoi_id=aoi_id,
                            status="completed",
                            metadata_path=metadata_path
                        )
                        session.add(ingest_job)
                        session.commit()
                        session.close()
                    except Exception as db_err:
                        print(f"[INFO] DB ingest job skipped: {db_err}")
                
                # Attempt NDVI aggregation if metadata file exists
                if metadata_path and PREPROC_AVAILABLE:
                    try:
                        agg_result = run_preproc.aggregate_ndvi(metadata_path)
                        ndvi_csv = agg_result.get("ndvi_csv")
                        ndvi_timeseries = agg_result.get("ndvi_timeseries")
                    except Exception as agg_err:
                        print(f"[INFO] NDVI aggregation skipped: {agg_err}")
                
                # Attempt NDVI raster computation if metadata file exists
                if metadata_path and PREPROC_AVAILABLE:
                    try:
                        raster_result = run_preproc.compute_raster(metadata_path)
                        ndvi_raster = raster_result.get("ndvi_raster")
                        parcel_confidence = raster_result.get("parcel_confidence")
                    except Exception as raster_err:
                        print(f"[INFO] NDVI raster computation skipped: {raster_err}")
                
                # Analyze all advanced signals and anomalies
                if ndvi_timeseries and PREPROC_AVAILABLE:
                    try:
                        anomalies = run_preproc.analyze_signals(ndvi_timeseries, ndvi_raster)
                    except Exception as sig_err:
                        print(f"[INFO] Advanced signals skipped: {sig_err}")
            
            except Exception as ingest_err:
                print(f"[INFO] Ingest failed, but continuing: {ingest_err}")
        
        # Update AOI record with report (thread-safe)
        aoi_record["status"] = "processed"
        aoi_record["metadata_path"] = metadata_path
        aoi_record["report"] = {
            "ndvi_csv": ndvi_csv,
            "ndvi_timeseries": ndvi_timeseries,
            "ndvi_raster": ndvi_raster,
            "parcel_confidence": parcel_confidence,
            "anomalies": anomalies
        }
        
        with AOI_STORE_LOCK:
            AOI_STORE[aoi_id_str] = aoi_record
        
        # Increment metrics counter if monitoring available
        if MONITORING_AVAILABLE:
            try:
                metrics.aoi_created_counter.inc()
            except Exception as metrics_err:
                print(f"[INFO] Metrics counter skipped: {metrics_err}")
        
        return {
            "aoi_id": aoi_id_str,
            "metadata_path": metadata_path,
            "ndvi_csv": ndvi_csv,
            "ndvi_timeseries": ndvi_timeseries,
            "ndvi_raster": ndvi_raster,
            "parcel_confidence": parcel_confidence,
            "anomalies": anomalies
        }
    
    except Exception as e:
        if MONITORING_AVAILABLE:
            try:
                metrics.aoi_error_counter.inc()
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/aoi/{aoi_id}/report", response_model=ReportResponse)
def get_aoi_report(aoi_id: str):
    """Get report for a previously created AOI"""
    
    with AOI_STORE_LOCK:
        if aoi_id not in AOI_STORE:
            raise HTTPException(status_code=404, detail="AOI not found")
        
        aoi_record = AOI_STORE[aoi_id]
    
    return {
        "aoi_id": aoi_id,
        "status": aoi_record.get("status", "unknown"),
        "metadata_path": aoi_record.get("metadata_path"),
        "report": aoi_record.get("report")
    }

# Mount optional monitoring endpoints
if MONITORING_AVAILABLE:
    try:
        app.mount("/metrics", metrics.metrics_app)
    except Exception as e:
        print(f"[INFO] Prometheus metrics not mounted: {e}")

# Optional startup event to initialize DB
@app.on_event("startup")
def startup():
    if DB_AVAILABLE:
        try:
            db.init_db()
            print("[INFO] Database initialized")
        except Exception as e:
            print(f"[INFO] Database initialization failed (optional): {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
