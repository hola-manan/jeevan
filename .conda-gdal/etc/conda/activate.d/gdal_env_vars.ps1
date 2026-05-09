$env:_OLD_GDAL_DATA = $env:GDAL_DATA
$env:_OLD_PROJ_LIB = $env:PROJ_LIB
$env:GDAL_DATA = Join-Path $env:CONDA_PREFIX "Library\share\gdal"
$env:PROJ_LIB = Join-Path $env:CONDA_PREFIX "Library\share\proj"
