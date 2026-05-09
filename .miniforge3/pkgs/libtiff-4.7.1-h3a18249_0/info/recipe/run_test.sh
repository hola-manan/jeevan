#!/bin/bash

set -ex

# Testing that binaries exist
test -f ${PREFIX}/bin/fax2ps
test -f ${PREFIX}/bin/fax2tiff
test -f ${PREFIX}/bin/pal2rgb
test -f ${PREFIX}/bin/ppm2tiff
test -f ${PREFIX}/bin/raw2tiff
test -f ${PREFIX}/bin/tiff2bw
test -f ${PREFIX}/bin/tiff2pdf
test -f ${PREFIX}/bin/tiff2ps
test -f ${PREFIX}/bin/tiff2rgba
test -f ${PREFIX}/bin/tiffcmp
test -f ${PREFIX}/bin/tiffcp
test -f ${PREFIX}/bin/tiffcrop
test -f ${PREFIX}/bin/tiffdither
test -f ${PREFIX}/bin/tiffdump
test -f ${PREFIX}/bin/tiffinfo
test -f ${PREFIX}/bin/tiffmedian
test -f ${PREFIX}/bin/tiffset
test -f ${PREFIX}/bin/tiffsplit

# Testing that static libraries don't exist
test ! -f ${PREFIX}/lib/libtiff.a
test ! -f ${PREFIX}/lib/libtiffxx.a

# Testing that headers exist
test -f ${PREFIX}/include/tiff.h
test -f ${PREFIX}/include/tiffconf.h
test -f ${PREFIX}/include/tiffio.h
test -f ${PREFIX}/include/tiffio.hxx

# Testing that dynamic librarires exist
test -f ${PREFIX}/lib/libtiff${SHLIB_EXT}
test -f ${PREFIX}/lib/libtiffxx${SHLIB_EXT}
# Soname can change and cause unforeseen problems for a few dowstream projects, so test it here.
if [[ "${target_platform}" == linux-* ]]; then
	test -f ${PREFIX}/lib/libtiff${SHLIB_EXT}.6
	test -f ${PREFIX}/lib/libtiffxx${SHLIB_EXT}.6
elif [[ "${target_platform}" == osx-* ]]; then
	test -f ${PREFIX}/lib/libtiff.6${SHLIB_EXT}
	test -f ${PREFIX}/lib/libtiffxx.6${SHLIB_EXT}
fi

# Testing that the pkgconfig file exists
test -f ${PREFIX}/lib/pkgconfig/libtiff-4.pc
