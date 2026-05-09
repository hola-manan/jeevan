"""
Agricultural signal helpers - numerical indices and stress detection
"""
import numpy as np
from typing import Dict, Any, List

# Vegetation indices

def ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """Normalized Difference Vegetation Index"""
    return (nir - red) / (nir + red + 1e-6)

def ndwi(green: np.ndarray, swir: np.ndarray) -> np.ndarray:
    """Normalized Difference Water Index"""
    return (green - swir) / (green + swir + 1e-6)

def evi(red: np.ndarray, nir: np.ndarray, blue: np.ndarray) -> np.ndarray:
    """Enhanced Vegetation Index"""
    return 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)

def savi(red: np.ndarray, nir: np.ndarray, L: float = 0.5) -> np.ndarray:
    """Soil-Adjusted Vegetation Index"""
    return ((nir - red) / (nir + red + L)) * (1 + L)

def ndre(red_edge: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """Normalized Difference Red Edge (red-edge NDVI)"""
    return (nir - red_edge) / (nir + red_edge + 1e-6)

def gci(nir: np.ndarray, green: np.ndarray) -> np.ndarray:
    """Green Chlorophyll Index"""
    return (nir / green) - 1

def msi(nir: np.ndarray, swir: np.ndarray) -> np.ndarray:
    """Moisture Stress Index"""
    return swir / nir

# Anomaly detection

def z_score_anomaly(values: np.ndarray, threshold: float = 2.0) -> np.ndarray:
    """
    Detect anomalies using z-score (standard deviations from mean).
    
    Args:
        values: Array of values
        threshold: Number of standard deviations (default 2.0 = ~95% confidence)
    
    Returns:
        Boolean array where True indicates anomaly
    """
    values = np.asarray(values, dtype=float)
    mean = np.nanmean(values)
    std = np.nanstd(values)
    if std == 0 or np.isnan(std):
        return np.zeros(values.shape, dtype=object)

    z_scores = np.abs((values - mean) / std)
    anomalies = z_scores >= threshold

    # Fallback to a robust modified z-score when a strong outlier inflates std
    # enough to mask itself in small samples.
    if not np.any(anomalies):
        median = np.nanmedian(values)
        mad = np.nanmedian(np.abs(values - median))
        if mad > 0 and not np.isnan(mad):
            modified_z = 0.6745 * np.abs(values - median) / mad
            anomalies = modified_z >= threshold

    return np.array([bool(flag) for flag in anomalies], dtype=object)

def ndvi_anomaly(ndvi_timeseries: List[float], threshold: float = 0.3) -> Dict[str, Any]:
    """
    Detect NDVI anomalies (rapid declines or low values).
    
    Args:
        ndvi_timeseries: List of NDVI values over time
        threshold: NDVI decline threshold for anomaly
    
    Returns:
        Dict with anomaly flag and details
    """
    
    if len(ndvi_timeseries) < 2:
        return {"anomaly": False, "reason": "insufficient_data"}
    
    ndvi_array = np.array(ndvi_timeseries)
    
    # Check for overall low NDVI
    mean_ndvi = np.nanmean(ndvi_array)
    if mean_ndvi < 0.3:
        return {
            "anomaly": True,
            "reason": "low_ndvi",
            "mean_ndvi": float(mean_ndvi)
        }
    
    # Check for rapid decline
    diffs = np.diff(ndvi_array)
    max_decline = np.min(diffs)
    
    if max_decline < -threshold:
        return {
            "anomaly": True,
            "reason": "rapid_decline",
            "max_decline": float(max_decline)
        }
    
    return {"anomaly": False}

# Stress detection

def irrigation_stress_flag(ndvi: float, lst: float = None) -> bool:
    """
    Flag potential irrigation stress using NDVI and Land Surface Temperature.
    
    High NDVI but high LST suggests water stress.
    
    Args:
        ndvi: NDVI value
        lst: Land Surface Temperature (optional)
    
    Returns:
        True if stress detected
    """
    
    if ndvi < 0.4:
        return True  # Low vegetation
    
    if lst is not None and lst > 35:
        return True  # High temperature + vegetation = stress
    
    return False

def persistent_stress_detection(
    ndvi_timeseries: List[float],
    window_size: int = 3
) -> Dict[str, Any]:
    """
    Detect persistent irrigation stress over time window.
    
    Args:
        ndvi_timeseries: Time series of NDVI values
        window_size: Window size for rolling statistics
    
    Returns:
        Dict with stress detection results
    """
    
    ndvi_array = np.array(ndvi_timeseries)
    
    if len(ndvi_array) < window_size:
        return {"persistent_stress": False}
    
    # Compute rolling mean
    rolling_mean = np.convolve(ndvi_array, np.ones(window_size) / window_size, mode='valid')
    
    # Detect windows with consistently low NDVI
    low_stress_windows = np.sum(rolling_mean < 0.4)
    stress_pct = low_stress_windows / len(rolling_mean) if len(rolling_mean) > 0 else 0
    
    persistent = bool(stress_pct > 0.5)
    
    return {
        "persistent_stress": persistent,
        "stress_window_pct": float(stress_pct),
        "low_stress_windows": int(low_stress_windows)
    }

def water_stress_score(ndvi: float, ndwi: float) -> float:
    """
    Compute water stress score combining NDVI and NDWI.
    
    Low NDVI + low NDWI = high stress.
    
    Args:
        ndvi: NDVI value
        ndwi: NDWI value
    
    Returns:
        Stress score 0-1 (0=no stress, 1=severe stress)
    """
    
    # Normalize to 0-1
    ndvi_norm = max(0, ndvi)  # NDVI typically -1 to 1
    ndwi_norm = max(0, ndwi)  # NDWI typically -1 to 1
    
    # Inverse: high vegetation/water = low stress
    stress = (1 - ndvi_norm) * 0.6 + (1 - ndwi_norm) * 0.4
    
    return float(np.clip(stress, 0, 1))

def nutrient_stress_score(ndvi: float, red_edge_ndvi: float) -> float:
    ndvi_norm = max(0.01, ndvi)
    re_norm = max(0.01, red_edge_ndvi)
    
    # Continuous formula: If NDRE is lagging far behind NDVI, stress is higher.
    # Typically NDRE is slightly lower than NDVI. A large gap means low chlorophyll.
    ratio = re_norm / ndvi_norm
    # Ideal ratio is ~0.6 to 0.8 depending on crop. 
    # If ratio is < 0.4, high stress. If ratio > 0.7, low stress.
    stress = 1.0 - ((ratio - 0.2) / 0.6)
    return float(np.clip(stress, 0.05, 0.95))

def parcel_confidence_score(
    mean_ndvi: float,
    ndvi_std: float,
    valid_pixel_pct: float
) -> float:
    """
    Compute overall parcel confidence based on NDVI statistics.
    
    Args:
        mean_ndvi: Mean NDVI across parcel
        ndvi_std: Standard deviation of NDVI
        valid_pixel_pct: Percentage of valid (non-cloud) pixels
    
    Returns:
        Confidence score 0-1
    """
    
    ndvi_score = min(1.0, max(0.0, (mean_ndvi + 1) / 2))
    uniformity = 1.0 - min(1.0, ndvi_std)
    validity = valid_pixel_pct / 100.0
    
    confidence = ndvi_score * 0.4 + uniformity * 0.3 + validity * 0.3
    
    return float(np.clip(confidence, 0, 1))
