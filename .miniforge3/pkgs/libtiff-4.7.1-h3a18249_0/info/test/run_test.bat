@echo on
setlocal EnableDelayedExpansion


@REM Testing executable files exist
if not exist %LIBRARY_BIN%\\fax2ps.exe exit 1
if not exist %LIBRARY_BIN%\\fax2tiff.exe exit 1
if not exist %LIBRARY_BIN%\\pal2rgb.exe exit 1
if not exist %LIBRARY_BIN%\\ppm2tiff.exe exit 1
if not exist %LIBRARY_BIN%\\raw2tiff.exe exit 1
if not exist %LIBRARY_BIN%\\tiff2bw.exe exit 1
if not exist %LIBRARY_BIN%\\tiff2pdf.exe exit 1
if not exist %LIBRARY_BIN%\\tiff2ps.exe exit 1
if not exist %LIBRARY_BIN%\\tiff2rgba.exe exit 1
if not exist %LIBRARY_BIN%\\tiffcmp.exe exit 1
if not exist %LIBRARY_BIN%\\tiffcp.exe exit 1
if not exist %LIBRARY_BIN%\\tiffcrop.exe exit 1
if not exist %LIBRARY_BIN%\\tiffdither.exe exit 1
if not exist %LIBRARY_BIN%\\tiffdump.exe exit 1
if not exist %LIBRARY_BIN%\\tiffinfo.exe exit 1
if not exist %LIBRARY_BIN%\\tiffmedian.exe exit 1
if not exist %LIBRARY_BIN%\\tiffset.exe exit 1
if not exist %LIBRARY_BIN%\\tiffsplit.exe exit 1

@REM Testing headers files exist
if not exist %LIBRARY_INC%\\tiff.h exit 1
if not exist %LIBRARY_INC%\\tiffconf.h exit 1
if not exist %LIBRARY_INC%\\tiffio.h exit 1
if not exist %LIBRARY_INC%\\tiffio.hxx exit 1
if not exist %LIBRARY_INC%\\tiffvers.h exit 1

@REM Testing dynamic libraries exist
if not exist %LIBRARY_BIN%\\tiff.dll exit 1
if not exist %LIBRARY_BIN%\\libtiff.dll exit 1
@REM The C++ tiffxx.dll has been removed as of 4.5.0:
@REM https://gitlab.com/libtiff/libtiff/-/merge_requests/338

@REM Testing import libraries exist
if not exist %LIBRARY_LIB%\\libtiff.lib exit 1
if not exist %LIBRARY_LIB%\\tiff.lib exit 1
if not exist %LIBRARY_LIB%\\tiffxx.lib exit 1

@REM Testing a pkgconfig file exists
if not exist %LIBRARY_LIB%\\pkgconfig\\libtiff-4.pc exit 1
