

@echo on

if not exist %LIBRARY_BIN%/libxml2.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
