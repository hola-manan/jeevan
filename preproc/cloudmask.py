"""
Cloud masking utilities for Sentinel-2
"""
import numpy as np

def scl_cloud_mask(scl_array: np.ndarray, cloud_classes: list = None) -> np.ndarray:
    """
    Create cloud mask from Sentinel-2 Scene Classification Layer (SCL).
    
    SCL classes:
    - 0: No Data
    - 1: Saturated or defective
    - 2: Dark Area Pixels
    - 3: Cloud Shadows
    - 4: Vegetation
    - 5: Not Vegetated
    - 6: Water
    - 7: Unclassified
    - 8: Cloud Medium Probability
    - 9: Cloud High Probability
    - 10: Thin Cirrus
    - 11: Snow
    
    Cloud classes default to: {3, 8, 9, 10} (cloud shadows, cloud medium/high, cirrus)
    
    Args:
        scl_array: SCL band array
        cloud_classes: List of SCL classes to mask (default cloud-related)
    
    Returns:
        Boolean mask (True = cloud/shadow, False = valid data)
    """
    
    if cloud_classes is None:
        cloud_classes = {3, 8, 9, 10}
    else:
        cloud_classes = set(cloud_classes)
    
    mask = np.isin(scl_array, list(cloud_classes))
    return mask

def qa60_mask(qa60_array: np.ndarray) -> np.ndarray:
    """
    Create cloud mask from Sentinel-2 QA60 band.
    
    QA60 is a 16-bit raster:
    - Bit 10: Cloud Probability (0=no clouds, 1=clouds)
    - Bit 11: Cirrus Probability (0=no cirrus, 1=cirrus)
    
    Args:
        qa60_array: QA60 band array (should be uint16)
    
    Returns:
        Boolean mask (True = cloud/cirrus, False = valid data)
    """
    
    # Extract cloud and cirrus bits
    cloud_bit = (qa60_array >> 10) & 1
    cirrus_bit = (qa60_array >> 11) & 1
    
    # Combine: mask pixels where either bit is set
    mask = (cloud_bit == 1) | (cirrus_bit == 1)
    
    return mask

def apply_mask(
    data_array: np.ndarray,
    mask: np.ndarray,
    fill_value: float = np.nan
) -> np.ndarray:
    """
    Apply cloud mask to data array.
    
    Args:
        data_array: Data array to mask
        mask: Boolean mask (True = bad, False = good)
        fill_value: Value to use for masked pixels
    
    Returns:
        Masked array
    """
    
    masked_data = data_array.astype(np.float32)
    masked_data[mask] = fill_value
    
    return masked_data
