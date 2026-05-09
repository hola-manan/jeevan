"""
Prometheus metrics for monitoring
"""
from prometheus_client import Counter, Histogram, make_asgi_app

# Define metrics
aoi_created_counter = Counter(
    'ashi_aoi_created_total',
    'Total number of AOIs created',
    ['status']
)

aoi_error_counter = Counter(
    'ashi_aoi_errors_total',
    'Total number of AOI creation errors'
)

request_duration_histogram = Histogram(
    'ashi_request_duration_seconds',
    'Request duration in seconds',
    ['endpoint']
)

# ASGI app for Prometheus metrics endpoint
metrics_app = make_asgi_app()
