



libdeflate-gzip -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
libdeflate-gunzip -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\\deflate.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\\deflate.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\\pkgconfig\\libdeflate.pc exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\\libdeflate.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
