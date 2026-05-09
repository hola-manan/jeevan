"""
Unified NDVI and cloud masking computation
"""
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any
from preproc import compute_ndvi, cloudmask

def compute_ndvi_with_mask(
    red_path: str,
    nir_path: str,
    scl_path: Optional[str] = None,
    qa60_path: Optional[str] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Compute NDVI with optional cloud masking.
    
    Args:
        red_path: Path to red band (B04) raster
        nir_path: Path to NIR band (B08) raster
        scl_path: Optional path to SCL (Scene Classification) band
        qa60_path: Optional path to QA60 band
        output_dir: Optional output directory for NDVI raster
    
    Returns:
        Dict with ndvi array, mask, and output path
    """
    
    try:
        import rasterio
    except ImportError:
        raise ImportError("rasterio required for raster I/O")
    
    # Read red and NIR bands
    with rasterio.open(red_path) as src:
        red_data = src.read(1)
        profile = src.profile
    
    with rasterio.open(nir_path) as src:
        nir_data = src.read(1)
    
    # Compute NDVI
    ndvi = compute_ndvi.compute_ndvi(red_data, nir_data)
    
    # Apply cloud mask if available
    mask = None
    if scl_path and Path(scl_path).exists():
        with rasterio.open(scl_path) as src:
            scl_data = src.read(1)
        mask = cloudmask.scl_cloud_mask(scl_data)
        ndvi = cloudmask.apply_mask(ndvi, mask)
    
    elif qa60_path and Path(qa60_path).exists():
        with rasterio.open(qa60_path) as src:
            qa60_data = src.read(1)
        mask = cloudmask.qa60_mask(qa60_data)
        ndvi = cloudmask.apply_mask(ndvi, mask)
    
    # Write output if requested
    output_path = None
    if output_dir:
        output_path = Path(output_dir) / "ndvi_masked.tif"
        profile.update(dtype=ndvi.dtype, count=1)
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(ndvi, 1)
    
    return {
        "ndvi": ndvi,
        "mask": mask,
        "output_path": str(output_path) if output_path else None
    }
