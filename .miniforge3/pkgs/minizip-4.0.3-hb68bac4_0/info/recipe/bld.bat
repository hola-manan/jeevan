@echo on

mkdir build
cd build

set CC=cl

cmake -G Ninja ^
  -DCMAKE_INSTALL_PREFIX="%LIBRARY_PREFIX%" ^
  -DBUILD_SHARED_LIBS=ON ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=ON ^
  -DMZ_FORCE_FETCH_LIBS=OFF ^
  -DMZ_BUILD_TESTS=OFF ^
  -DMZ_BUILD_UNIT_TESTS=OFF ^
  -DMZ_COMPAT=ON ^
  -DMZ_ZLIB=ON ^
  -DMZ_BZIP2=ON ^
  -DMZ_LMZA=ON ^
  -DMZ_ZSTD=ON ^
  -DMZ_LIBCOMP=OFF ^
  -DMZ_OPENSSL=OFF ^
  -DMZ_ICONV=OFF ^
  ..
if %ERRORLEVEL% neq 0 exit 1

cmake --build .
if %ERRORLEVEL% neq 0 exit 1

cmake --install .
if %ERRORLEVEL% neq 0 exit 1

cd ..
