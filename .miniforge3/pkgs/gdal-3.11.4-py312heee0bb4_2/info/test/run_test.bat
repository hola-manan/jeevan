

@echo on

python test_python.py
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal2tiles --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal2xyz --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_calc --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_edit --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_fillnodata --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_merge --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_pansharpen --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_polygonize --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_proximity --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_retile --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdal_sieve --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdalattachpct --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdalcompare --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
gdalmove --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
pct2rgb --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
rgb2pct --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
ogrmerge --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
ogr_layer_algebra --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
