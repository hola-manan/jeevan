:: Activation script
mkdir "%PREFIX%\etc\conda\activate.d"
COPY "%RECIPE_DIR%\activate.bat" "%PREFIX%\etc\conda\activate.d\vs%YEAR%_compiler_vars.bat"
pushd "%PREFIX%\etc\conda\activate.d"
sed -i 's/@YEAR@/%YEAR%/g' vs%YEAR%_compiler_vars.bat
sed -i 's/@VER@/%VER%/g' vs%YEAR%_compiler_vars.bat
sed -i 's/@update_version@/%update_version%/g' vs%YEAR%_compiler_vars.bat
sed -i 's/@cross_compiler_target_platform@/%cross_compiler_target_platform%/g' vs%YEAR%_compiler_vars.bat
sed -i 's/@tools_version@/%tools_version%/g' vs%YEAR%_compiler_vars.bat
sed -i 's/@msvc_version@/%msvc_version%/g' vs%YEAR%_compiler_vars.bat
popd

:: Deactivation script
mkdir %PREFIX%\etc\conda\deactivate.d
copy %RECIPE_DIR%\deactivate.bat %PREFIX%\etc\conda\deactivate.d\~vs%YEAR%_compiler_deactivate.bat
