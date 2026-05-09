"""
NDVI computation from red and NIR bands
"""
import numpy as np
from typing import Union, Optional, Tuple
from pathlib import Path

def compute_ndvi(
    red_array: np.ndarray,
    nir_array: np.ndarray,
    output_path: Optional[str] = None
) -> Union[np.ndarray, str]:
    """
    Compute NDVI from red and NIR raster arrays.
    
    NDVI = (NIR - Red) / (NIR + Red)
    
    Args:
        red_array: Red band array
        nir_array: NIR band array
        output_path: Optional path to write output raster
    
    Returns:
        NDVI array if output_path is None, otherwise output_path string
    """
    
    # Convert to float to avoid integer division issues
    red = red_array.astype(np.float32)
    nir = nir_array.astype(np.float32)
    
    # Compute NDVI
    numerator = nir - red
    denominator = nir + red
    
    # Avoid division by zero
    ndvi = np.zeros_like(numerator)
    mask = denominator != 0
    ndvi[mask] = numerator[mask] / denominator[mask]
    
    # Write to file if path provided
    if output_path:
        try:
            import rasterio
            from rasterio.transform import Affine
            
            # Simple transform (would need proper geotransform in production)
            transform = Affine.identity()
            
            with rasterio.open(
                output_path,
                'w',
                driver='GTiff',
                height=ndvi.shape[0],
                width=ndvi.shape[1],
                count=1,
                dtype=ndvi.dtype,
                transform=transform
            ) as dst:
                dst.write(ndvi, 1)
            
            return str(output_path)
        except ImportError:
            print("[WARN] rasterio not available, returning array")
            return ndvi
    
    return ndvi
