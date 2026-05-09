

@echo on

f2py -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -c "import numpy; numpy.show_config()"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set OPENBLAS_NUM_THREADS=1
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest -ra -vv -n auto --pyargs numpy -k "not slow and not (_not_a_real_test or test_exp2)" --durations=50 --durations-min=1.0
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
