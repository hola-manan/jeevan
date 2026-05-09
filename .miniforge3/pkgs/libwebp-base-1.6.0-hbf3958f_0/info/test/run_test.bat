



if not exist %LIBRARY_LIB%\libwebp.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\libwebp.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\libwebpdemux.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\libwebpdemux.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\libwebpmux.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\libwebpmux.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\libwebpdecoder.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\libwebpdecoder.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\libsharpyuv.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\libsharpyuv.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_PREFIX%\WebP\cmake\WebPConfig.cmake exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\webp\decode.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\webp\demux.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\webp\encode.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\webp\mux_types.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\webp\mux.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\webp\types.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\cwebp.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\dwebp.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\gif2webp.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\img2webp.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\webpinfo.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\webpmux.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
