@echo off
set "_OLD_GDAL_DATA=%GDAL_DATA%"
set "_OLD_PROJ_LIB=%PROJ_LIB%"
set "GDAL_DATA=%CONDA_PREFIX%\Library\share\gdal"
set "PROJ_LIB=%CONDA_PREFIX%\Library\share\proj"
