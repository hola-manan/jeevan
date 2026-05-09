@echo on
:: Set env vars that tell distutils to use the compiler that we put on path
SET DISTUTILS_USE_SDK=1
:: This is probably not good. It is for the pre-UCRT msvccompiler.py *not* _msvccompiler.py
SET MSSdk=1

SET "VS_VERSION=@VER@.@update_version@"
SET "VS_MAJOR=@VER@"
SET "VS_YEAR=@YEAR@"

set "MSYS2_ARG_CONV_EXCL=/AI;/AL;/OUT;/out"
set "MSYS2_ENV_CONV_EXCL=CL"

:: For Python 3.5+, ensure that we link with the dynamic runtime.  See
:: http://stevedower.id.au/blog/building-for-python-3-5-part-two/ for more info
set "PY_VCRUNTIME_REDIST=%PREFIX%\bin\vcruntime140.dll"

:: set CC and CXX for cmake
set "CXX=cl.exe"
set "CC=cl.exe"

set "VSINSTALLDIR="
:: Try to find actual vs2022 installations
for /f "usebackq tokens=*" %%i in (`vswhere.exe -nologo -products * -version ^[17.0^,18.0^] -property installationPath`) do (
  :: There is no trailing back-slash from the vswhere, and may make vcvars64.bat fail, so force add it
  set "VSINSTALLDIR=%%i\"
)
if not exist "%VSINSTALLDIR%" (
    :: VS2022 install but with vs2017/vs2019 compiler stuff installed
	for /f "usebackq tokens=*" %%i in (`vswhere.exe -nologo -products * -requires Microsoft.VisualStudio.Component.VC.v@msvc_version@.x86.x64 -property installationPath`) do (
	:: There is no trailing back-slash from the vswhere, and may make vcvars64.bat fail, so force add it
	set "VSINSTALLDIR=%%i\"
	)
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Professional\"
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Community\"
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\"
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Enterprise\"
)

IF NOT "%CONDA_BUILD%" == "" (
  set "INCLUDE=%LIBRARY_INC%;%INCLUDE%"
  set "LIB=%LIBRARY_LIB%;%LIB%"
  set "CMAKE_PREFIX_PATH=%LIBRARY_PREFIX%;%CMAKE_PREFIX_PATH%"
) else (
  :: normal environment
  set "INCLUDE=%CONDA_PREFIX%\Library\include;%INCLUDE%"
  set "LIB=%CONDA_PREFIX%\Library\lib;%LIB%"
  set "CMAKE_PREFIX_PATH=%CONDA_PREFIX%\Library;%CMAKE_PREFIX_PATH%"
)


call :GetWin10SdkDir
:: dir /ON here is sorting the list of folders, such that we use the latest one that we have
for /F %%i in ('dir /ON /B "%WindowsSdkDir%\include"') DO (
  if NOT "%%~i" == "wdf" (
    SET WindowsSDKVer=%%~i
  )
)
if errorlevel 1 (
    echo "Didn't find any windows 10 SDK. I'm not sure if things will work, but let's try..."
) else (
    echo Windows SDK version found as: "%WindowsSDKVer%"
)

IF "@cross_compiler_target_platform@" == "win-64" (
  set "BITS=64"
  set "CMAKE_PLAT=Win64"
) else (
  set "BITS=32"
  set "CMAKE_PLAT=Win32"
)

pushd %VSINSTALLDIR%
set VSCMD_DEBUG=1
CALL "VC\Auxiliary\Build\vcvars%BITS%.bat" -vcvars_ver=@tools_version@ %WindowsSDKVer%
popd

:: CMAKE configuration
:: See: https://cmake.org/cmake/help/latest/generator/Visual%20Studio%2017%202022.html
:: See: https://cmake.org/cmake/help/latest/variable/CMAKE_GENERATOR_TOOLSET.html
:: See: https://cmake.org/cmake/help/latest/variable/CMAKE_GENERATOR_PLATFORM.html
set "CMAKE_GEN=Visual Studio @VER@ @YEAR@"
IF "%CMAKE_GENERATOR%" == "" SET "CMAKE_GENERATOR=%CMAKE_GEN%"
IF "%CMAKE_GENERATOR_PLATFORM%" == "" SET "CMAKE_GENERATOR_PLATFORM=%CMAKE_PLAT%"
IF "%CMAKE_GENERATOR_TOOLSET%" == "" SET "CMAKE_GENERATOR_TOOLSET=v@msvc_version@"

:GetWin10SdkDir
call :GetWin10SdkDirHelper HKLM\SOFTWARE\Wow6432Node > nul 2>&1
if errorlevel 1 call :GetWin10SdkDirHelper HKCU\SOFTWARE\Wow6432Node > nul 2>&1
if errorlevel 1 call :GetWin10SdkDirHelper HKLM\SOFTWARE > nul 2>&1
if errorlevel 1 call :GetWin10SdkDirHelper HKCU\SOFTWARE > nul 2>&1
if errorlevel 1 exit /B 1
exit /B 0


:GetWin10SdkDirHelper
@REM `Get Windows 10 SDK installed folder`
for /F "tokens=1,2*" %%i in ('reg query "%1\Microsoft\Microsoft SDKs\Windows\v10.0" /v "InstallationFolder"') DO (
    if "%%i"=="InstallationFolder" (
        SET WindowsSdkDir=%%~k
    )
)
exit /B 0
