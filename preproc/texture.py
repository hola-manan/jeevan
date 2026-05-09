"""
Texture metrics for spatial analysis
"""
import numpy as np
from typing import Dict, Any

def local_std(data: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Compute local standard deviation using convolution.
    
    Args:
        data: Input 2D array
        kernel_size: Size of local window (default 3x3)
    
    Returns:
        Array of local standard deviations
    """
    
    try:
        from scipy.ndimage import generic_filter
        return generic_filter(data, np.std, size=kernel_size)
    except ImportError:
        # Fallback: simple block-wise approximation
        return _local_std_fallback(data, kernel_size)

def local_entropy(data: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Compute local Shannon entropy using convolution.
    
    Low entropy = uniform (homogeneous)
    High entropy = diverse (heterogeneous)
    
    Args:
        data: Input 2D array
        kernel_size: Size of local window
    
    Returns:
        Array of local entropy values
    """
    
    try:
        from scipy.ndimage import generic_filter
        return generic_filter(data, _shannon_entropy, size=kernel_size)
    except ImportError:
        # Fallback: simple block-wise approximation
        return _local_entropy_fallback(data, kernel_size)

def _shannon_entropy(values):
    """Compute Shannon entropy of a local window"""
    # Normalize to histogram
    hist, _ = np.histogram(values, bins=10, range=(0, 1))
    hist = hist / (np.sum(hist) + 1e-10)
    
    # Compute entropy
    entropy = -np.sum(hist * np.log2(hist + 1e-10))
    
    return entropy

def _local_std_fallback(data: np.ndarray, kernel_size: int) -> np.ndarray:
    """Fallback local std computation without scipy"""
    
    pad_size = kernel_size // 2
    padded = np.pad(data, pad_size, mode='edge')
    
    output = np.zeros_like(data)
    
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            window = padded[i:i+kernel_size, j:j+kernel_size]
            output[i, j] = np.std(window)
    
    return output

def _local_entropy_fallback(data: np.ndarray, kernel_size: int) -> np.ndarray:
    """Fallback local entropy computation without scipy"""
    
    pad_size = kernel_size // 2
    padded = np.pad(data, pad_size, mode='edge')
    
    output = np.zeros_like(data, dtype=np.float32)
    
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            window = padded[i:i+kernel_size, j:j+kernel_size].flatten()
            output[i, j] = _shannon_entropy(window)
    
    return output
