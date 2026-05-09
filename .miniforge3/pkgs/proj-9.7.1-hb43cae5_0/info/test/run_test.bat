



if not exist %LIBRARY_LIB%\\proj.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1

IF %ERRORLEVEL% NEQ 0 exit /B 1
echo -105 40 | proj +proj=utm +zone=13 +ellps=WGS84
IF %ERRORLEVEL% NEQ 0 exit /B 1
echo -117 30 | cs2cs +proj=latlong +datum=NAD27 +to +proj=latlong +datum=NAD83
IF %ERRORLEVEL% NEQ 0 exit /B 1
echo -105 40 | cs2cs +init=epsg:4326 +to +init=epsg:2975
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
