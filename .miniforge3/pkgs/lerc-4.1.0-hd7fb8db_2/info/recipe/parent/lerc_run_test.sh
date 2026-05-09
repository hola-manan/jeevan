#!/bin/bash
set -ex

# Compile and run upstream's full encode/decode test against the just-built
# libLerc. Catches linker/symbol/encoding regressions before ship.
${CXX} -std=c++17 ${CXXFLAGS} ${LDFLAGS} \
    -I"${PREFIX}/include" -L"${PREFIX}/lib" \
    "${SRC_DIR}/src/LercTest/main.cpp" \
    -lLerc -o LercTest

LERCTEST_NONINTERACTIVE=1 \
    LD_LIBRARY_PATH="${PREFIX}/lib:${LD_LIBRARY_PATH:-}" \
    DYLD_LIBRARY_PATH="${PREFIX}/lib:${DYLD_LIBRARY_PATH:-}" \
    ./LercTest
