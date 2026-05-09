set PATH=%PREFIX%\cmake-bin\bin;%PATH%

REM Configure step
copy jconfig.vc jconfig.h
if errorlevel 1 exit /b 1

mkdir %c_compiler%
pushd %c_compiler%
set CXXFLAGS=
set CFLAGS=

REM Build step
cmake -G "NMake Makefiles"                     ^
      -DCMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX%  ^
      -DCMAKE_BUILD_TYPE=Release               ^
      ..

if errorlevel 1 exit /b 1
cmake --build . --config Release --target INSTALL -- VERBOSE=1
if errorlevel 1 exit /b 1

REM This allows consuming build systems to use the -ljpeg option,
REM which is also specified in the .pc file.
REM the .dll remains called libjpeg.dll to ensure previously-built
REM downstream packages don't fail at runtime.
copy %PREFIX%\Library\lib\libjpeg.lib %PREFIX%\Library\lib\jpeg.lib

popd
