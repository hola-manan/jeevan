cd build
if errorlevel 1 exit 1

rd /s /q swig\python

FOR /F "tokens=*" %%g IN ('%PYTHON% -c "import numpy; print(numpy.get_include())"') do (SET Python_NumPy_INCLUDE_DIR=%%g)

cmake "-UPython*" "-U*LATER_PLUGIN" ^
      -DCMAKE_BUILD_TYPE=Release ^
      -DPython_EXECUTABLE="%PYTHON%" ^
      -DPython_NumPy_INCLUDE_DIR="%Python_NumPy_INCLUDE_DIR%" ^
      -DGDAL_PYTHON_INSTALL_PREFIX:PATH="%STDLIB_DIR%\.." ^
      -DBUILD_PYTHON_BINDINGS:BOOL=ON ^
      "%SRC_DIR%"
if errorlevel 1 exit /b 1

cmake --build . --target python_generated_files
if errorlevel 1 exit /b 1

cd swig\python
if errorlevel 1 exit /b 1

:: Have to use `setup.py install` here to make sure pip creates *.exe files for console_scripts without absolute paths
:: to invalid python interpreters.
%PYTHON% setup.py install
if errorlevel 1 exit /b 1
