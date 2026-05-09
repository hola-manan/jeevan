

@echo on

echo "tests done during build ..."
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
