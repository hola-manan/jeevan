@echo off
setlocal enabledelayedexpansion

cd %SRC_DIR%\OtherLanguages\Python

%PYTHON% -m pip install . --no-deps --no-build-isolation -vv
