



djpeg -dct int -ppm -outfile testout.ppm testorig.jpg
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%/Library/lib/pkgconfig/libjpeg.pc exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%/Library/bin/libjpeg.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%/Library/lib/libjpeg.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%/Library/lib/jpeg.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%/Library/lib/jpeg-static.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%/Library/include/jpeglib.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
