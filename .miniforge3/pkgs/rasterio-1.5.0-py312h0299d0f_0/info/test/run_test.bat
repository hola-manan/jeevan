

@echo on

pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
rio --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
rio info test_data\\test.tif
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
