#!/bin/bash

set -ex

mkdir -p build-cpp
pushd build-cpp

cmake -GNinja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_PREFIX_PATH=$PREFIX \
      -DCMAKE_INSTALL_LIBDIR=lib \
      -DCMAKE_INSTALL_PREFIX=$PREFIX \
      -DCMAKE_C_FLAGS="$CFLAGS" \
      -DCMAKE_POSITION_INDEPENDENT_CODE=on \
      -DURIPARSER_BUILD_DOCS=off \
      -DURIPARSER_BUILD_TOOLS=off \
      -DBUILD_SHARED_LIBS=on \
      -DURIPARSER_BUILD_TESTS=on \
      -DURIPARSER_BUILD_WCHAR_T=on \
      -DURIPARSER_BUILD_CHAR=on \
      ..

cmake --build . --config Release --target install

# CMAKE: URIPARSER_BUILD_TESTS=ON requires both URIPARSER_BUILD_CHAR=ON and URIPARSER_BUILD_WCHAR_T=ON.
ctest --output-on-failure -j${CPU_COUNT}

popd
