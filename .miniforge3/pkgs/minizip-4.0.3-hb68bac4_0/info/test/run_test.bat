



if not exist %LIBRARY_BIN%\libminizip.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\libminizip.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
