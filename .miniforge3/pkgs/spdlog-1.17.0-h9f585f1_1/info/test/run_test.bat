



if not exist %PREFIX%\Library\include\spdlog\spdlog.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
