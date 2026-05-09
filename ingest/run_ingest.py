"""
Stub ingest implementation - simple metadata JSON writer
"""
import json
import os
from datetime import datetime
from pathlib import Path

def stub_ingest(aoi_geojson, start_date=None, end_date=None, aoi_id=None):
    """
    Stub ingest path - writes demo metadata JSON.
    
    Args:
        aoi_geojson: AOI geometry as GeoJSON dict
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        aoi_id: AOI ID for naming
    
    Returns:
        dict with metadata_path and other ingest metadata
    """
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create metadata payload
    metadata = {
        "aoi": aoi_geojson,
        "start_date": start_date,
        "end_date": end_date,
        "fetched_at": datetime.utcnow().isoformat(),
        "tiles": [
            {
                "tile_id": "31TCG",
                "date": "2024-03-15",
                "cloud_percentage": 12.5
            },
            {
                "tile_id": "31TCG",
                "date": "2024-04-14",
                "cloud_percentage": 5.2
            }
        ]
    }
    
    # Write metadata JSON
    metadata_filename = f"ingest_metadata_{aoi_id or 'demo'}.json"
    metadata_path = data_dir / metadata_filename
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return {
        "metadata_path": str(metadata_path),
        "success": True
    }
