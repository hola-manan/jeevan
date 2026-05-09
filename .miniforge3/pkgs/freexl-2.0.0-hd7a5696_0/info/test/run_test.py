#  tests for freexl-2.0.0-hd7a5696_0 (this is a generated file);
print('===== testing package: freexl-2.0.0-hd7a5696_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---

# just load libfreexl using ctypes
import os
import sys
import ctypes

if sys.platform == 'win32':
    libfreexl = ctypes.CDLL('freexl.dll')
elif sys.platform == 'darwin':
    # LD_LIBRARY_PATH not set on OSX or Linux
    path = os.path.expandvars('$PREFIX/lib/libfreexl.dylib')
    libfreexl = ctypes.CDLL(path)
else:
    path = os.path.expandvars('$PREFIX/lib/libfreexl.so')
    libfreexl = ctypes.CDLL(path)
    #  --- run_test.py (end) ---

print('===== freexl-2.0.0-hd7a5696_0 OK =====');
