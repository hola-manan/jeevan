



pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest -v -k "not test_filename_formatting" tests
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
