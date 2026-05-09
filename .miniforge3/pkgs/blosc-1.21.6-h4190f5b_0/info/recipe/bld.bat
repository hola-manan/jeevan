setlocal EnableDelayedExpansion

mkdir build
if %ERRORLEVEL% neq 0 exit 1
cd build
if %ERRORLEVEL% neq 0 exit 1

cmake -G "NMake Makefiles" ^
      -DCMAKE_BUILD_TYPE:STRING="Release" ^
      -DCMAKE_INSTALL_PREFIX:PATH="%LIBRARY_PREFIX%" ^
      -DCMAKE_PREFIX_PATH:PATH="%LIBRARY_PREFIX%" ^
      -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON ^
      -DBUILD_STATIC:BOOL=ON ^
      -DBUILD_SHARED:BOOL=ON ^
      -DBUILD_TESTS:BOOL=ON ^
      -DBUILD_BENCHMARKS:BOOL=OFF ^
      -DPREFER_EXTERNAL_LZ4:BOOL=ON ^
      -DPREFER_EXTERNAL_ZLIB:BOOL=ON ^
      -DPREFER_EXTERNAL_ZSTD:BOOL=ON ^
      "%SRC_DIR%"
if %ERRORLEVEL% neq 0 exit 1

cmake --build . --config Release
if %ERRORLEVEL% neq 0 exit 1

ctest -C release
if %ERRORLEVEL% neq 0 exit 1

cmake --build . --target INSTALL --config Release
if %ERRORLEVEL% neq 0 exit 1
