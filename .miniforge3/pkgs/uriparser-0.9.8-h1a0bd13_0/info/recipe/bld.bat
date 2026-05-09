@echo on

mkdir build-cpp
if errorlevel 1 exit 1

cd build-cpp

cmake -GNinja ^
      -DCMAKE_BUILD_TYPE=Release ^
      -DCMAKE_PREFIX_PATH=%CONDA_PREFIX% ^
      -DCMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX% ^
      -DCMAKE_POSITION_INDEPENDENT_CODE=on ^
      -DURIPARSER_BUILD_DOCS=off ^
      -DURIPARSER_BUILD_TOOLS=off ^
      -DBUILD_SHARED_LIBS=on ^
      -DURIPARSER_BUILD_TESTS=on ^
      -DURIPARSER_BUILD_WCHAR_T=on ^
      -DURIPARSER_BUILD_CHAR=on ^
      ..
if errorlevel 1 exit 1

cmake --build . --config Release --target install
if errorlevel 1 exit 1

REM CMAKE: URIPARSER_BUILD_TESTS=ON requires both URIPARSER_BUILD_CHAR=ON and URIPARSER_BUILD_WCHAR_T=ON.
ctest --output-on-failure
if errorlevel 1 exit 1