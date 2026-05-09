



pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest -vv . --ignore=tests/test_diagram.py -k "not (TestExamples or Test02_WithoutPackrat or Test04_WithPackrat or Test06_WithBoundedPackrat or Test08_WithUnboundedPackrat or Test09_WithLeftRecursionParsing or Test10_WithLeftRecursionParsingBoundedMemo)"
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
