mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=${PREFIX}  \
      -DCMAKE_PREFIX_PATH=${PREFIX}     \
      $SRC_DIR
ctest
make install -j${CPU_COUNT} ${VERBOSE_CM}
