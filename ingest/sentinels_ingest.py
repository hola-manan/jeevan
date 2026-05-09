
import json
import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from . import run_ingest

def ingest(
    aoi_geojson: dict,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    aoi_id: Optional[str] = None
) -> Dict[str, Any]:
    try:
        geometry = aoi_geojson.get("features", [{}])[0].get("geometry", None)
        if not geometry:
            raise ValueError("No geometry found")
            
        if not start_date: start_date = "2024-01-01"
        if not end_date: end_date = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Planetary Computer STAC
        stac_url = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
        payload = {
            "collections": ["sentinel-2-l2a"],
            "intersects": geometry,
            "datetime": f"{start_date}T00:00:00Z/{end_date}T23:59:59Z",
            "query": {"eo:cloud_cover": {"lt": 50}},
            "limit": 100
        }
        
        print("[INFO] Querying Planetary Computer STAC API...")
        response = requests.post(stac_url, json=payload, timeout=30)
        response.raise_for_status()
        stac_results = response.json()
        features = stac_results.get("features", [])
        print(f"[INFO] Found {len(features)} satellite passes.")
        
        # Get SAS token for data access
        token_url = "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a"
        sas_token = requests.get(token_url).json().get("token", "")
        
        # Append SAS token to all asset hrefs
        if sas_token:
            for feat in features:
                for asset_key, asset_val in feat.get("assets", {}).items():
                    href = asset_val.get("href", "")
                    if href:
                        asset_val["href"] = f"{href}?{sas_token}"
        
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        metadata = {
            "aoi": aoi_geojson,
            "start_date": start_date,
            "end_date": end_date,
            "fetched_at": datetime.utcnow().isoformat(),
            "stac_items": features
        }
        
        metadata_filename = f"ingest_metadata_{aoi_id or 'stac'}.json"
        metadata_path = data_dir / metadata_filename
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return {"metadata_path": str(metadata_path), "success": True, "products_found": len(features)}
        
    except Exception as e:
        print(f"[WARN] PC STAC query failed: {e}")
        return run_ingest.stub_ingest(aoi_geojson, start_date, end_date, aoi_id)
