

@echo on

if not exist %PREFIX%\\Library\\bin\\openblas.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %PREFIX%\\Library\\lib\\openblas.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
