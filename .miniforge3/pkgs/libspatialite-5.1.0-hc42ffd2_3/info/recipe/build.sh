#!/bin/bash

# make sure arm64 is a known host ...
cp -r ${BUILD_PREFIX}/share/libtool/build-aux/config.* .
export LDFLAGS="-L${PREFIX}/lib ${LDFLAGS}"

# these files have hardcoded paths in them.  We don't need .la files anyway, so just remove it.
if [ -f ${PREFIX}/${HOST}/lib/libstdc++.la ]; then
    find ${PREFIX} -name "*.la" -print0 | xargs -0 rm
fi

# Disabling geos 3.10 and 3.11 as we are building against geos 3.9
# Disabling rttopo and gcp as both modules strictly depend on code released under the GPLv2+
  ./configure --prefix=${PREFIX} \
              --host=${HOST} \
              --build=${BUILD} \
              --enable-static=no \
              --enable-geos3100=no \
              --enable-geos3110=no \
              --disable-rttopo \
              --disable-gcp \
              --enable-minizip=yes

make
make check || (cat test/test-suite.log; exit 1)
make install
