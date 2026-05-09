#  tests for xerces-c-3.3.0-h885b0b7_0 (this is a generated file);
print('===== testing package: xerces-c-3.3.0-h885b0b7_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import os
import sys
import ctypes

version = os.getenv("PKG_VERSION")
vstring = '_'.join(version.split('.')[:2])

if sys.platform == 'win32':
    lib = ctypes.CDLL('xerces-c_%s.dll' % vstring)
elif sys.platform == 'darwin':
    # LD_LIBRARY_PATH not set on OSX or Linux
    path = os.path.expandvars('$PREFIX/lib/libxerces-c.dylib')
    lib = ctypes.CDLL(path)
else:
    path = os.path.expandvars('$PREFIX/lib/libxerces-c.so')
    lib = ctypes.CDLL(path)
#  --- run_test.py (end) ---

print('===== xerces-c-3.3.0-h885b0b7_0 OK =====');
