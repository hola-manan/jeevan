#!/bin/bash
set -ex

mkdir cmake_build
cd cmake_build

cmake ${CMAKE_ARGS} -LAH              \
    -DCMAKE_BUILD_TYPE=Release        \
    -DCMAKE_INSTALL_PREFIX=$PREFIX    \
    -DCMAKE_INSTALL_LIBDIR=lib        \
    -DBUILD_SHARED_LIBS=ON            \
    ..

make -j${CPU_COUNT}
make install
