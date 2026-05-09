



if not exist %PREFIX%\\Library\\bin\\uriparser.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\lib\\cmake\\uriparser-0.9.8\\uriparser.cmake exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\include\\uriparser\\Uri.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\include\\uriparser\\UriBase.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\include\\uriparser\\UriDefsAnsi.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\include\\uriparser\\UriDefsConfig.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\include\\uriparser\\UriDefsUnicode.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\include\\uriparser\\UriIp4.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
