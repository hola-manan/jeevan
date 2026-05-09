

@echo on

pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -c "from importlib.metadata import version; assert(version('attrs')=='26.1.0')"
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest --fixtures tests -vv
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
