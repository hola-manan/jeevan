"""
SAR (Synthetic Aperture Radar) helper functions
"""
import numpy as np
from typing import Dict, Any

def sar_db_to_linear(sar_db: np.ndarray) -> np.ndarray:
    """Convert SAR dB values to linear scale"""
    return 10 ** (sar_db / 10)

def sar_linear_to_db(sar_linear: np.ndarray) -> np.ndarray:
    """Convert SAR linear values to dB scale"""
    sar_linear = np.asarray(sar_linear, dtype=float)
    if np.any(sar_linear <= 0):
        raise ValueError("sar_linear values must be positive")
    return 10 * np.log10(sar_linear)

def sar_vh_vv_difference(vh: np.ndarray, vv: np.ndarray) -> np.ndarray:
    """
    Compute VH-VV difference in dB.
    
    VH (cross-pol) / VV (co-pol) ratio is sensitive to vegetation structure.
    
    Args:
        vh: VH polarization (cross-pol) in dB
        vv: VV polarization (co-pol) in dB
    
    Returns:
        VH-VV difference
    """
    return vh - vv

def sar_moisture_index(sar_stack: np.ndarray, temporal_window: int = 3) -> np.ndarray:
    """
    Compute SAR-based moisture index from temporal stack.
    
    Moisture increases SAR backscatter in certain frequency bands.
    Uses temporal median to reduce speckle.
    
    Args:
        sar_stack: Time series of SAR observations (time x height x width)
        temporal_window: Window size for temporal filtering
    
    Returns:
        Moisture index array
    """
    
    if len(sar_stack.shape) != 3:
        raise ValueError("sar_stack must be 3D (time, height, width)")
    
    # Compute temporal median to reduce speckle noise
    temporal_median = np.median(sar_stack, axis=0)
    
    # Simple moisture proxy: median backscatter intensity
    # Higher SAR backscatter = more moisture (in some frequency ranges)
    moisture_index = temporal_median / (np.max(temporal_median) + 1e-6)
    
    return moisture_index

def sar_stack_loading(
    sar_file_paths: list,
    normalize: bool = True
) -> np.ndarray:
    """
    Load and stack multiple SAR observations.
    
    Args:
        sar_file_paths: List of paths to SAR rasters
        normalize: Whether to normalize each layer
    
    Returns:
        Stacked SAR array (time x height x width)
    """
    
    try:
        import rasterio
    except ImportError:
        raise ImportError("rasterio required for SAR loading")
    
    sar_stack = []
    
    for file_path in sar_file_paths:
        with rasterio.open(file_path) as src:
            sar_data = src.read(1).astype(np.float32)
            
            if normalize:
                sar_data = (sar_data - np.nanmean(sar_data)) / (np.nanstd(sar_data) + 1e-6)
            
            sar_stack.append(sar_data)
    
    return np.stack(sar_stack, axis=0)
