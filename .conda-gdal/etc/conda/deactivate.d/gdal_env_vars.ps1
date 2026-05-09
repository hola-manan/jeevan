if ($null -ne $env:_OLD_GDAL_DATA -and $env:_OLD_GDAL_DATA -ne "") {
    $env:GDAL_DATA = $env:_OLD_GDAL_DATA
} else {
    Remove-Item Env:GDAL_DATA -ErrorAction SilentlyContinue
}
if ($null -ne $env:_OLD_PROJ_LIB -and $env:_OLD_PROJ_LIB -ne "") {
    $env:PROJ_LIB = $env:_OLD_PROJ_LIB
} else {
    Remove-Item Env:PROJ_LIB -ErrorAction SilentlyContinue
}
Remove-Item Env:_OLD_GDAL_DATA -ErrorAction SilentlyContinue
Remove-Item Env:_OLD_PROJ_LIB -ErrorAction SilentlyContinue
