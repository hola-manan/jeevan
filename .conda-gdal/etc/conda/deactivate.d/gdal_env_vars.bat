@echo off
if defined _OLD_GDAL_DATA (
    set "GDAL_DATA=%_OLD_GDAL_DATA%"
) else (
    set "GDAL_DATA="
)
if defined _OLD_PROJ_LIB (
    set "PROJ_LIB=%_OLD_PROJ_LIB%"
) else (
    set "PROJ_LIB="
)
set "_OLD_GDAL_DATA="
set "_OLD_PROJ_LIB="
