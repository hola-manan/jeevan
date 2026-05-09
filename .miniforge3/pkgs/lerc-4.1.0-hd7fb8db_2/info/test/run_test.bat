@echo on

REM Compile and run upstream's full encode/decode test against the just-built
REM Lerc.dll. Catches linker/symbol/encoding regressions before ship.
cl /nologo /std:c++17 /EHsc /MD                 ^
    /I "%LIBRARY_INC%"                          ^
    "%SRC_DIR%\src\LercTest\main.cpp"           ^
    /link /LIBPATH:"%LIBRARY_LIB%" Lerc.lib /OUT:LercTest.exe
if errorlevel 1 exit 1

set "LERCTEST_NONINTERACTIVE=1"
set "PATH=%LIBRARY_BIN%;%PATH%"
LercTest.exe
if errorlevel 1 exit 1


@echo on

if not exist %LIBRARY_INC%\Lerc_types.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_INC%\Lerc_c_api.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_BIN%\Lerc.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\Lerc.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_LIB%\pkgconfig\Lerc.pc exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
