



if not exist %LIBRARY_LIB%\\geotiff_i.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\\geotiff.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
